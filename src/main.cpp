#include "mainwindow.h"
#include <QApplication>

#pragma push_macro("slots")
#undef slots
#include <Python.h>
#pragma pop_macro("slots")

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
