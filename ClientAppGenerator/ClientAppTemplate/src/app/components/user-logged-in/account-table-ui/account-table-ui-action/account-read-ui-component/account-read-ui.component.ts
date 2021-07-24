import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AccountService, Account } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "app-account-read-ui-component",
  templateUrl: "./account-read-ui.component.html",
  styleUrls: ["./account-read-ui.component.scss"],
})

export class AccountReadUIComponent implements OnInit {
  service: AccountService;
  isDarkThemeSubscription: boolean=false;
  item: Account;
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject(AccountService) srv: AccountService,
    private route: ActivatedRoute) {
    this.service = srv;
    this.checkTheme();
    this.idSelectedInputNumber = -1;
  }

  ngOnInit(): void {
    this.idSelectedInput = this.route.snapshot.paramMap.get('id');
    this.idSelectedInputNumber = (+ this.idSelectedInput);
    this.getItemById();
  }

  getItemById() {
    this.service.apiAccountIdGet(this.idSelectedInput).subscribe(data => {
      this.item = data;
    })
  }

  checkTheme() {
    this.themeService.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem('dark') == 'true') {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }
}
