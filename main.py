from controller import Controller
import signal



def main():
    obj = Controller()
    signal.signal(signal.SIGINT, obj.sigint_handler)
    obj.run()


if __name__ == '__main__':
    main()