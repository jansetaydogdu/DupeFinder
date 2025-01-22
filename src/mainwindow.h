#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QCompleter>
#include <qmessagebox.h>
#include "embed.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_lineEdit_textChanged(const QString &arg1);

    void on_listView_activated(const QModelIndex &index);

    void on_listView_clicked(const QModelIndex &index);

    void on_lineEdit_editingFinished();

    void on_pushButton_clicked();

    void on_autoCompleteView_activated(const QModelIndex &index);

    void on_autoCompleteView_clicked(const QModelIndex &index);

    void on_inputBox2_textChanged(const QString &arg1);

    void on_pushButton_2_clicked();

    void on_resultWidget_itemSelectionChanged();

    void select(qsizetype index = 0);

private:
    Ui::MainWindow *ui;
    QCompleter *completer;
    QVector<ProductDataFrame> resultList;
};
#endif // MAINWINDOW_H
