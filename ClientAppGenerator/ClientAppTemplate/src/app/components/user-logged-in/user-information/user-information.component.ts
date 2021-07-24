import { Component, OnInit } from '@angular/core';
import { ThemeServiceService } from 'src/app/style-service/theme-service.service';

@Component({
  selector: 'app-user-information',
  templateUrl: './user-information.component.html',
  styleUrls: ['./user-information.component.scss'],
})
export class UserInformationComponent implements OnInit {
  isDarkThemeSubscription: boolean = false;
  constructor(private themeSerive: ThemeServiceService) {}

  ngOnInit(): void {
    this.checkTheme();
  }
  checkTheme() {
    this.themeSerive.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem('dark') == 'true') {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }
}
