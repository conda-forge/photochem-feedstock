import glob
import os
import subprocess
import sysconfig

def main():
    platlib = sysconfig.get_path("platlib")
    pattern = os.path.join(platlib, "photochem", "*.so")
    libs = sorted(set(glob.glob(pattern)))
    print("Found libs:", libs)
    if not libs:
        raise SystemExit(f"No photochem shared libraries found under {pattern}")

    bad = False
    for lib in libs:
        out = subprocess.check_output(["readelf", "-W", "-l", lib], text=True)
        if any(("GNU_STACK" in line and "E" in line) for line in out.splitlines()):
            print("ERROR: executable stack detected:", lib)
            bad = True
        else:
            print("OK: non-executable stack:", lib)

    raise SystemExit(1 if bad else 0)

if __name__ == "__main__":
    main()
