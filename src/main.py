import sys
import asyncio
import qasync
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

# Export MainWindow directly
__all__ = ['MainWindow']

async def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Keep the event loop running
    await qasync.QEventLoop(app).run_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)