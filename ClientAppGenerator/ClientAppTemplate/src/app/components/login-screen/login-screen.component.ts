import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login-screen',
  templateUrl: './login-screen.component.html',
  styleUrls: ['./login-screen.component.scss'],
})
export class LoginScreenComponent implements OnInit {
  displayScreen: String = 'login';
  constructor() {}

  ngOnInit(): void {}
  switchForm(screen: any): void {
    this.displayScreen = screen;
  }
}
