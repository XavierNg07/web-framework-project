# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def application(environ, start_response):
    response_body = [
        f'{key}: {value}' for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    application()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
