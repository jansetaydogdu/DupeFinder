#include "embed.h"
#include <qfile.h>
#include <QString>
#include <QStringList>
#include <QMessageBox>
#include <QRegularExpression>

#pragma push_macro("slots")
#undef slots
#include <Python.h>
#pragma pop_macro("slots")


ProductDataFrame::ProductDataFrame(QString productName, QString productCategory, QStringList productIngredients, int productMatchScore)
    : name{ productName }
    , category{ productCategory }
    , ingredients{ productIngredients }
    , matchScore{ productMatchScore }
{
}

QStringList dfExpression(QString unformattedInput)
{
    QStringList parts;
    unformattedInput = unformattedInput.trimmed();
    static const QRegularExpression regex{"\"([^\"]*)\"|[^,]+"};
    QRegularExpressionMatchIterator i = regex.globalMatch(unformattedInput);
    while (i.hasNext()) {
        QRegularExpressionMatch match = i.next();
        QString matchedText = match.captured(1).trimmed();
        if (matchedText.isEmpty()) {
            matchedText = match.captured(0).trimmed();
        }
        parts << matchedText;
    }

    // name = parts[0];
    // category = parts[1];
    // ingredients = parts[2];
    // matchscore = parts[3];

    return parts;
}

QVector<ProductDataFrame> dfSearchResult(QString csvPath){
    QVector<ProductDataFrame> dfFromCsv{ };
    QFile file{ csvPath };
    if( !file.open(QIODevice::ReadOnly) ){ QMessageBox::information(0, "Error", file.errorString()); }

    QTextStream in{ &file };
    while( !in.atEnd() )
    {
        QStringList dfCurrent{ dfExpression(in.readLine()) };
        if( dfCurrent.length() == 4 ){ dfFromCsv.push_back( ProductDataFrame(dfCurrent[0], dfCurrent[1], dfCurrent[2].split("  "), dfCurrent[3].toInt() )); }
    }

    return dfFromCsv;
}

void callDupeFinder(QStringList args){
    QString searchArgs{" 'dupeFinderCli.py', 'searchToCsv' "};
    if(args.length() <= 1){ args.append("water  "); }
    for(const QString& arg : args){ searchArgs.append( ",\'" + arg.trimmed() + '\'' ); }
    QString pyScript = QString(
        "dupeFinderCli.main( argc=%1, argv=[ %2 ] )"
    ).arg( QString::number(args.length()+1), searchArgs );
    PyRun_SimpleString( pyScript.toStdString().c_str() );
}

void updateLists(){
    PyRun_SimpleString("dupeFinderCli.updateList()");
    PyRun_SimpleString("dupeFinderCli.writeLists()");
}

QStringList readLists()
{
    QStringList autoCompleteLists;
    QStringList *categoryList{ readCategories() };
    QStringList *ingredientList{ readIngredients() };

    for(const QString& category : *categoryList){ autoCompleteLists.append(category); }
    for(const QString& ingredient : *ingredientList){ autoCompleteLists.append(ingredient); }

    delete categoryList;
    delete ingredientList;
    return autoCompleteLists;
}

QStringList *readProducts(QString path)
{
    QStringList *products = new QStringList{};

    QFile file{ path };
    if( !file.open(QIODevice::ReadOnly) ){ QMessageBox::information(0, "Error", file.errorString()); }

    QTextStream in{ &file };
    while( !in.atEnd() ){ products->append( in.readLine() ); }

    file.close();
    return products;
}

QStringList *readCategories(QString path)
{
    QStringList *categories = new QStringList{};

    QFile file{ path };
    if( !file.open(QIODevice::ReadOnly) ){ QMessageBox::information(0, "Error", file.errorString()); }

    QTextStream in{ &file };
    while( !in.atEnd() ){ categories->append( in.readLine() ); }

    file.close();
    return categories;
}

QStringList *readIngredients(QString path)
{
    QStringList *ingredients{ nullptr };

    QFile file{ path };
    if( !file.open(QIODevice::ReadOnly) ){ QMessageBox::information(0, "Error", file.errorString()); }

    QString mergedIngredients = file.readLine();
    ingredients = new QStringList{ mergedIngredients.split(",") };
    for (QString& unformattedIngredient : *ingredients) {
        while (!unformattedIngredient.isEmpty() && !unformattedIngredient.at(0).isLetterOrNumber()) {
            unformattedIngredient.remove(0, 1);
        }
        while (!unformattedIngredient.isEmpty() && !unformattedIngredient.at(unformattedIngredient.length() - 1).isLetterOrNumber()) {
            unformattedIngredient.remove(unformattedIngredient.length() - 1, 1);
        }
    }

    return ingredients;
}
