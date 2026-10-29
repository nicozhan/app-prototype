#!/usr/bin/env python3
"""无头 Chrome 截图后从 786 宽裁出中间 393px（iPhone 15 逻辑宽度）。
用法: python3 crop.py <输入png> <输出png>"""
import zlib, struct, sys


def read_png(fn):
    d = open(fn, 'rb').read()
    pos, idat = 8, b''
    w = h = ct = None
    while pos < len(d):
        ln = struct.unpack('>I', d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        chunk = d[pos + 8:pos + 8 + ln]
        if typ == b'IHDR':
            w, h, bit, ct = struct.unpack('>IIBB', chunk[:10])
            assert bit == 8 and ct in (2, 6), (bit, ct)
        elif typ == b'IDAT':
            idat += chunk
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = 4 if ct == 6 else 3
    stride = w * ch
    out = bytearray()
    prev = bytearray(stride)
    i = 0
    for _ in range(h):
        f = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                b = prev[x]
                c = prev[x - ch] if x >= ch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out += line
        prev = line
    return w, h, ch, bytes(out)


def write_png(fn, w, h, ch, pix):
    ct = 6 if ch == 4 else 2
    raw = b''.join(b'\x00' + pix[y * w * ch:(y + 1) * w * ch] for y in range(h))

    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)

    open(fn, 'wb').write(
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, ct, 0, 0, 0))
        + chunk(b'IDAT', zlib.compress(raw, 6))
        + chunk(b'IEND', b''))


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    w, h, ch, pix = read_png(src)
    x0 = (w - 393) // 2
    rows = [pix[(y * w + x0) * ch:(y * w + x0 + 393) * ch] for y in range(h)]
    write_png(dst, 393, h, ch, b''.join(rows))
    print(f'{src} ({w}x{h}) -> {dst} (393x{h})')
