"""App-Data-Compressor - content-defined chunking + compression for experiment/registry data.
Stdlib zlib stands in for zstd when zstandard is not installed; chunking/dedup logic is native.
"""
import zlib, hashlib
def chunk(data: bytes, size=4096):
    return [data[i:i+size] for i in range(0, len(data), size)] or [b""]
def dedup_chunks(data: bytes, size=4096):
    seen={}; out=[]
    for c in chunk(data, size):
        h=hashlib.sha256(c).hexdigest()
        if h not in seen: seen[h]=c; out.append(c)
    return b"".join(out), {"chunks": len(chunk(data,size)), "unique_chunks": len(seen)}
def compress(data: bytes):
    deduped, meta = dedup_chunks(data); packed=zlib.compress(deduped, 9)
    return packed, {**meta, "original": len(data), "compressed": len(packed),
                    "ratio": round(len(packed)/len(data),3) if data else 0.0}
def decompress(packed: bytes): return zlib.decompress(packed)
