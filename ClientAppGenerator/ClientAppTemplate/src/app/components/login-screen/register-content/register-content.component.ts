import { Component, OnInit } from '@angular/core';
import {
  AuthService,
  UserRegisterRequest,
} from '@hqhoangvuong/api-client-803868';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-register-content',
  templateUrl: './register-content.component.html',
  styleUrls: ['./register-content.component.scss'],
})
export class RegisterContentComponent implements OnInit {
  userName: string;
  email: string;
  password: string;
  firstName: string;
  middleName: string;
  lastName: string;
  phoneNumber: string;
  private show: boolean=false

  userRegister: UserRegisterRequest = {
    username: '',
    email: '',
    password: '',
    firstName: '',
    middleName: '',
    lastName: '',
    phoneNumber: ''
  };
  constructor(private authService: AuthService, private toast: ToastrService) {}

  ngOnInit(): void {}
  onRegisterUser() {
    this.userRegister.email = this.email;
    this.userRegister.password = this.password;
    this.userRegister.username = this.userName;
    this.userRegister.phoneNumber = this.phoneNumber;
    this.userRegister.firstName = this.firstName;
    this.userRegister.middleName = this.middleName;
    this.userRegister.lastName = this.lastName;
    this.authService.apiAuthRegisterPost(this.userRegister).subscribe(
      (data) => {
        this.toast.success('Register successfully', 'Information');
      },
      (err) => {
        this.toast.success(err, 'Warning');
      }
    );
  }
  onResetForm() {
    this.userName = '';
    this.email = '';
    this.password = '';
    this.phoneNumber = '';
    this.firstName = '';
    this.middleName = '';
    this.lastName = '';
  }
}
