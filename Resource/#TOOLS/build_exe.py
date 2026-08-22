import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "HMOL资源文档生成器"
TMP = os.path.join(HERE, ".tmp-install")


def run(cmd, env=None):
    print(">", " ".join(cmd) if isinstance(cmd, list) else cmd)
    try:
        subprocess.check_call(cmd, env=env)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    print("=" * 52)
    print("  HMOL 资源文档生成器 - 一键打包脚本")
    print("=" * 52)

    try:
        subprocess.check_call([sys.executable, "--version"], stdout=subprocess.DEVNULL)
    except Exception:
        print("[错误] 未检测到 Python，请先安装 Python 3.10+")
        return 1

    try:
        subprocess.check_call(
            [sys.executable, "-m", "PyInstaller", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[OK] PyInstaller 已安装")
    except Exception:
        print("[提示] 未检测到 PyInstaller，正在安装...")
        if not run([sys.executable, "-m", "pip", "install", "pyinstaller"]):
            print("[错误] PyInstaller 安装失败，请手动执行: pip install pyinstaller")
            return 1

    os.makedirs(TMP, exist_ok=True)
    env = os.environ.copy()
    env["TMP"] = TMP
    env["TEMP"] = TMP

    print("\n[1/3] 开始打包...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name",
        NAME,
        "--distpath",
        HERE,
        "--workpath",
        os.path.join(TMP, "pyinstaller-build"),
        "--specpath",
        TMP,
        os.path.join(HERE, "md_creator.py"),
    ]
    if not run(cmd, env=env):
        print("[错误] 打包失败，请检查上方日志")
        return 1

    print("\n[2/3] 清理中间文件...")
    shutil.rmtree(os.path.join(TMP, "pyinstaller-build"), ignore_errors=True)
    spec = os.path.join(TMP, NAME + ".spec")
    if os.path.exists(spec):
        os.remove(spec)
    pycache = os.path.join(HERE, "__pycache__")
    if os.path.isdir(pycache):
        shutil.rmtree(pycache, ignore_errors=True)

    exe = os.path.join(HERE, NAME + ".exe")
    print("\n[3/3] 打包完成！")
    print(f"    exe 已生成：{exe}")
    if os.path.exists(exe):
        size = os.path.getsize(exe) / 1024 / 1024
        print(f"    大小：{size:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
