#ifndef EMBED_H
#define EMBED_H

#include <QString>
#include <QStringList>

class ProductDataFrame
{
public:
    ProductDataFrame(QString name, QString category, QStringList productIngredients, int productMatchScore);
    QString getName(){ return name; }
    QString getCategory(){ return category; }
    QStringList getIngredients(){ return ingredients; }
    int getMatchScore(){ return matchScore; }
private:
    QString name{};
    QString category{};
    QStringList ingredients{};
    int matchScore;
};

QVector<ProductDataFrame> dfSearchResult(QString csvPath = "../src/data/searchResults.csv");
QStringList readLists();
QStringList *readProducts(QString path = "../src/lists/products.txt" );
QStringList *readCategories(QString path = "../src/lists/categories.txt");
QStringList *readIngredients(QString path = "../src/lists/ingredients.txt");
void callDupeFinder(QStringList args);
void updateLists();

#endif // EMBED_H
