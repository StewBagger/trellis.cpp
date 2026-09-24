"""Print the Intel Xe flash-attention gate's inputs once, to find what rejects Battlemage."""
import sys, pathlib

f = pathlib.Path("thirdparty/ggml/src/ggml-vulkan/ggml-vulkan.cpp")
s = f.read_text(encoding="utf-8")
needle = "xe_fa_opt = xe_fa_supported_platform && xe_fa_supported_usage && xe_fa_supported_dtype;"
if needle not in s:
    sys.exit("anchor not found in ggml-vulkan.cpp")

dbg = needle + r"""
        { static int once = 0; if (!once) { once = 1;
            fprintf(stderr, "[XEFA] arch=%d devID=0x%X | plat=%d usage=%d dtype=%d | neq0=%d nev0=%d hasmask=%d | qnb1=%zu qnb2=%zu knb1=%zu knb2=%zu vnb1=%zu vnb2=%zu | qt=%d kt=%d vt=%d mt=%d\n",
              (int)ctx->device.get()->architecture, (unsigned)ctx->device.get()->properties.deviceID,
              (int)xe_fa_supported_platform, (int)xe_fa_supported_usage, (int)xe_fa_supported_dtype,
              (int)neq0, (int)nev0, (int)(mask != nullptr),
              (size_t)q->nb[1], (size_t)q->nb[2], (size_t)k->nb[1], (size_t)k->nb[2],
              (size_t)v->nb[1], (size_t)v->nb[2],
              (int)q->type, (int)k->type, (int)v->type, (int)(mask ? mask->type : -1));
        } }"""

f.write_text(s.replace(needle, dbg, 1), encoding="utf-8")
print("instrumented ggml-vulkan.cpp")
