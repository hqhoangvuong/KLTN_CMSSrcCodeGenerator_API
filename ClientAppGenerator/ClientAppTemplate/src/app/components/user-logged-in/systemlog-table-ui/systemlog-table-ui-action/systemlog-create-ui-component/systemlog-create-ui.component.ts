import { Component, Inject, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';
import { SystemLogService, SystemLog, AccountService,  Account,  } from '@hqhoangvuong/api-client-803868';
import { HttpHeaders } from "@angular/common/http";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-systemlog-create-ui-component",
  templateUrl: "./systemlog-create-ui.component.html",
  styleUrls: ["./systemlog-create-ui.component.scss"],
})

export class SystemLogcreateUIComponent implements OnInit {
  isDarkThemeSubscription: boolean = false;
  entityDisplayName = "Create";
  isContinueToCreate: boolean = true;
  service: SystemLogService;
  item: SystemLog;
  accountItems: Account[] = [];

  accountService: AccountService;

  itemSeleted: any;
  token: any;

  constructor(
    private themeSerive: ThemeServiceService,
    private route: Router,
    @Inject(SystemLogService) srv: SystemLogService,
    @Inject(AccountService) accountsrv:  AccountService,

    private toast: ToastrService
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
    accountsrv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as SystemLog;
    this.service = srv;
    this.accountService = accountsrv;

    this.checkTheme();
  }

  checkTheme() {
    this.themeSerive.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem("dark") == "true") {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }

  ngOnInit(): void {
    this.ddlDataBinding();
  }

  ddlDataBinding(): void {
    this.accountService.apiAccountGet().subscribe((result) => {
      this.accountItems = result;
    })

  }

  createNewItem() {
    this.service.apiSystemLogPost(this.item).subscribe(
      (data) => {
        this.toast.success("Create new SystemLog successfully", "Information");
      },
      (err) => {
        this.toast.warning("Something wrong happen", "Warning");
      }
    );

    if (!this.isContinueToCreate) {
      this.route.navigate(['/user/index/systemlogmanagement']);
    }
  }
}
