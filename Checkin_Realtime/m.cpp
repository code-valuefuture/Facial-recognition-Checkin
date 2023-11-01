/*
Tài khoản khách hàng 
Cho cấu trúc có tên TaiKhoan để lưu trữ dữ liệu sau về tài khoản khách hàng như sau:
struct TaiKhoan
{
	char HoTen[30];		//Họ vàTên khách hàng
	char DiaChi[30];		//Địa chỉ
	char DienThoai[10];		//Số điện thoại
	float SoDu;			//Số dư tài khoản
};
Yêu cầu: 
Viết chương trình thực hiện:
-	Cho phép người dùng nhập vào n tài khoản khách hàng với n nhập từ bàn phím.
-	Cho người dùng nhập vào 1 vị trí muốn sửa. Sau đó cho người dùng nhập lại thông tin tài khoản và
 gán lại thông tin tương ứng. 
-	Ghi thông tin tất cả tài khoản khách hàng vào tệp nhị phân có tên TaiKhoan.dat.
*/

#include <iostream>
#include<fstream>
using namespace std;

struct TaiKhoan
{
	char HoTen[30];		
	char DiaChi[30];		
	char DienThoai[10];	
	float SoDu;			
};
int main()
{
  int n;
  cout<<"Nhap n: ";
  cin>>n;

  TaiKhoan o[n];
  for(int i=0;i<n;i++)
  {
    TaiKhoan o[i];
    cout<<"Nhap ten: ";
    cin.ignore();
    cin.getline(o[i].HoTen,30);
    cout<<"Nhap dia chi: ";
    cin.ignore();
    cin.getline(o[i].DiaChi,30);
    cout<<"Nhap dien thoai: ";
    cin.ignore();
    cin.getline(o[i].DienThoai,10);
    cout<<"Nhap So du: ";
    cin>>o[i].SoDu;
  }
  int vt;
  cout<<"Nhap vao vi tri muon sua: ";
  cin>>vt;
  cout<<"Nhap ten: ";
  cin.ignore();
  cin.getline(o[vt].HoTen,30);
  cout<<"Nhap dia chi: ";
  cin.ignore();
  cin.getline(o[vt].DiaChi,30);
  cout<<"Nhap dien thoai: ";
  cin.ignore();
  cin.getline(o[vt].DienThoai,10);
  cout<<"Nhap So du: ";
  cin>>o[vt].SoDu;
  
  ofstream out ("TaiKhoan.dat",ios::binary);
  out.write(reinterpret_cast<char*>(o),n* sizeof("TaiKhoan.dat"));

}
