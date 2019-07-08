#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "dm_reader.h"

#include <QMainWindow>
#include <QFile>
#include <QFileDialog>
#include <iostream>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_selectFolder_clicked();

private:
    Ui::MainWindow *ui;
    DM_Reader *decoder;
    QString parent_dir = "";
};

#endif // MAINWINDOW_H
