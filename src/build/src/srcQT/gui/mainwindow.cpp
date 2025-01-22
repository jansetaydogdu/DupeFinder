#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <QColor>
#include <QColorDialog>
#include <QAbstractProxyModel>
#include <QCompleter>
#include <QStringList>
#include <QDebug>
#include <QListView>
#include <qmessagebox.h>
#include "embed.h"

#pragma push_macro("slots")
#undef slots
#include <Python.h>
#pragma pop_macro("slots")

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , completer{ new QCompleter( readLists() , this) }
    , resultList{ }
{
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('../src')");
    PyRun_SimpleString("import dupeFinderCli");
    ui->setupUi(this);
    ui->listView->hide();
    ui->autoCompleteView->hide();
    completer->setCaseSensitivity(Qt::CaseInsensitive);
    completer->setFilterMode(Qt::MatchContains);
    showMaximized();
}

MainWindow::~MainWindow()
{
    Py_Finalize();
    delete ui;
    delete completer;
}

void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{
    ui->listView->hide();
    if( !ui->lineEdit->text().isEmpty() )
    {
        QStringList args = arg1.split(',');
        QString currentArg = args.last().trimmed();
        if(currentArg.length() > 2){
            completer->setCompletionPrefix(currentArg);
            ui->listView->setModel( completer->completionModel() );
            ui->listView->show();
        }
    }
}


void autoComplete(const QModelIndex &index, QLineEdit *lineEdit){
    QString currentString = lineEdit->text();
    QString::ConstIterator lastCommaIndex = currentString.cbegin() + currentString.lastIndexOf(',') + 1;
    currentString.erase( lastCommaIndex, currentString.cend() );
    lineEdit->setText( currentString + index.data().toString() + ',' );
}

void MainWindow::on_listView_clicked(const QModelIndex &index){ autoComplete(index, ui->lineEdit); }
void MainWindow::on_listView_activated(const QModelIndex &index){ autoComplete(index, ui->lineEdit); }

bool clicked(QLineEdit *lineEdit, QListWidget *listWidget, QVector<ProductDataFrame> *resultList)
{
    if(lineEdit->text().length() <= 0){
        lineEdit->setPlaceholderText( lineEdit->placeholderText()+'!' );
        return false;
    }
    QString searchString{ lineEdit->text().trimmed() };
    callDupeFinder( searchString.split(',') );
    *resultList = dfSearchResult();
    if(resultList->length() <= 0){
        QMessageBox::information(
            nullptr,
            "No Results",
            "Sorry, no results with your wanted ingredients were found. Perhaps try adding more alternative ingredients."
        );
        return false;
    }
    listWidget->clear();
    for(auto &elem : *resultList){ listWidget->addItem(elem.getName()); }
    return true;
}

void MainWindow::select(qsizetype index){
    ProductDataFrame dfCurrent = resultList[ index ];
    ui->msgBad->hide();
    ui->msgDecent->hide();
    ui->msgGood->hide();
    if( dfCurrent.getMatchScore() <= 0.30*resultList[0].getMatchScore() ){ ui->msgBad->show(); }
    else if( dfCurrent.getMatchScore() <= 0.60*resultList[0].getMatchScore() ){ ui->msgDecent->show(); }
    else{ ui->msgGood->show(); }

    ui->gName->setText( dfCurrent.getName() );
    ui->gCategory->setText( "Category:\n" + dfCurrent.getCategory() );
    ui->gIngredients->setText( "Ingredients:\n" + dfCurrent.getIngredients().join(", ") );
}

void MainWindow::on_pushButton_clicked(){
    if( clicked(ui->lineEdit, ui->resultWidget, &resultList) )
    {
        select(0);
        QString searchString{ ui->lineEdit->text() };
        ui->inputBox2->setText( searchString );
        ui->stackedWidget->setCurrentIndex(1);
    }
}
void MainWindow::on_pushButton_2_clicked(){
    clicked(ui->inputBox2, ui->resultWidget, &resultList);
}

void MainWindow::on_autoCompleteView_clicked(const QModelIndex &index){ autoComplete(index, ui->inputBox2); }
void MainWindow::on_autoCompleteView_activated(const QModelIndex &index){ autoComplete(index, ui->inputBox2); }

void MainWindow::on_inputBox2_textChanged(const QString &arg1)
{
    ui->autoCompleteView->hide();
    if( !ui->lineEdit->text().isEmpty() )
    {
        QStringList args = arg1.split(',');
        QString currentArg = args.last().trimmed();
        qDebug() << currentArg;
        if(currentArg.length() > 2){
            completer->setCompletionPrefix(currentArg);
            ui->autoCompleteView->setModel( completer->completionModel() );
            ui->autoCompleteView->show();
        }
    }
}


void MainWindow::on_lineEdit_editingFinished(){ }
void MainWindow::on_resultWidget_itemSelectionChanged(){ select( ui->resultWidget->currentRow() ); }

