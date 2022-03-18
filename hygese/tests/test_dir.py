import hygese, subprocess, os

def test_dir():
    print("Hello Dir!")
    print("hygese.HGS_LIBRARY_FILEPATH = ", hygese.HGS_LIBRARY_FILEPATH)
    subprocess.check_call('ls')
    os.listdir() 
    os.listdir("hygese")

    a = 10
    assert a == 10