class test:
    def __init__(self) -> None:
        self.b=1
    


def main():
    my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    my_string = str(my_dict)
    print(type(my_string))

if __name__ == '__main__':
    main()