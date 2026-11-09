from storage import ROOT

assert (ROOT / "user.json").is_file()
print("PASS: 01_exists")
