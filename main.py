from menu import *

if __name__ == '__main__':
    m = Menu()
    try:
        m.run()
    finally:
        pygame.quit()
        sys.exit()