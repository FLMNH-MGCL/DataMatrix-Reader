#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    decoder = nullptr;
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_selectFolder_clicked()
{
    parent_dir.clear();
    parent_dir = QFileDialog::getExistingDirectory();

    // std::cout << parent_dir.toUtf8().constData() << std::endl;
    QChar last_char = parent_dir[parent_dir.length() - 1];

    if (last_char != '/' || last_char != '\\') {
        parent_dir += '/';
    }

    // std::cout << parent_dir.toUtf8().constData() << std::endl;
    decoder = new DM_Reader(parent_dir.toUtf8().constData());
    decoder->Decode("/home/aaron/Documents/data_science/DataMatrix-Reader/images/test/test.png");
    std::cout << "PASSED DECODE" << std::endl;
}
