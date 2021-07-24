import { Time } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { AuthService, LoginRequest } from '@hqhoangvuong/api-client-803868';
import * as moment from 'moment';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login-content',
  templateUrl: './login-content.component.html',
  styleUrls: ['./login-content.component.scss'],
})
export class LoginContentComponent implements OnInit {
  private currentTime: any;
  private greeting: string;
  userName: any;
  password: any;
  user: LoginRequest = {
    email: '',
    password: '',
  };
  constructor(private Authent: AuthService, private toast: ToastrService) {}

  ngOnInit(): void {
    this.activateClock();
    this.getGreeting();
  }

  activateClock(): void {
    setInterval(() => {
      var date = moment.utc().format();
      this.currentTime = moment.utc(date).local().format('HH : mm : ss ');
    }, 1000);
  }

  getGreeting(): void{
    var date = moment.utc().format();
    let currentHour = Number.parseInt(moment(date).local().format("HH : mm : ss"));
    if (currentHour >= 3 && currentHour < 12) {
        this.greeting = "Good Morning";
    } else if (currentHour >= 12 && currentHour < 15){
      this.greeting= "Good Afternoon";
    }   else if (currentHour >= 15 && currentHour < 20){
      this.greeting=  "Good Evening";
    } else {
      this.greeting= "Good Night";
    } 
  }

  onSubmitUser() {
    this.user.email = this.userName;
    this.user.password = this.password;
    this.Authent.apiAuthLoginPost(this.user).subscribe(
      (sucess) => {
        this.toast.success(
          'Login to system successfuuly',
          'EasyWeb: Information'
        );
        localStorage.setItem('accessToken', sucess.accessToken);
        window.location.href = '/user';
      },
      (error) => {
        console.log(error);
        this.toast.error('Login user not successfully', 'EasyWeb: Error');
      }
    );
  }
}
