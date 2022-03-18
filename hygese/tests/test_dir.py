import hygese, subprocess

def test_dir():
    print("Hello Dir!")
    print(hygese.HGS_LIBRARY_FILEPATH)
    subprocess.check_call('ls')
