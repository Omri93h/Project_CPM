from Controller.controller import Controller as ctrl
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def main():
    controller = ctrl()
    controller.run()


if __name__ == '__main__':
    main()

main()