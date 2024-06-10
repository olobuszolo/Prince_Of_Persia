from menu import *
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
if __name__ == '__main__':
    m = Menu()
    try:
        m.run()
    finally:
        pygame.quit()
        sys.exit()