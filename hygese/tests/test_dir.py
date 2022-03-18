import hygese, subprocess, os

def test_dir():

    print("Hello Dir!")

    print(__file__)
    
    print("hygese.HGS_LIBRARY_FILEPATH = ", hygese.HGS_LIBRARY_FILEPATH)
    subprocess.check_call('ls')

    print("--------------[.]---------------")
    d = os.listdir() 
    print(d)
    for f in d:
        print(f)
        

    print("--------------[hygese]---------------")
    d = os.listdir("hygese") 
    print(d)
    for f in d:
        print(f)

    print("--------------[..]---------------")
    d = os.listdir("..") 
    print(d)
    for f in d:
        print(f)


    a = 10
    assert a == 10