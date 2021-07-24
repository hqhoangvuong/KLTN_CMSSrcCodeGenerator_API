import { Component, OnInit, Inject, Input } from "@angular/core";
import { Router, ActivatedRoute, ParamMap } from "@angular/router";
import { SystemLogService, SystemLog, AccountService,  Account,  } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from "../../../../../style-service/theme-service.service";
import { ToastrService } from "ngx-toastr";
import { HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-systemlog-update-ui-component",
  templateUrl: "./systemlog-update-ui.component.html",
  styleUrls: ["./systemlog-update-ui.component.scss"],
})
export class SystemLogUpdateUIComponent implements OnInit {
  idSelectedInput = '';
  idSelectedInputNumber: number;
  isDarkThemeSubscription: boolean = false;
  service: SystemLogService;
  item: SystemLog;
  token: any;
  accountItems: Account[] = [];

  accountService: AccountService;


  constructor(
    private themeService: ThemeServiceService,
    @Inject(SystemLogService) srv: SystemLogService,
    @Inject(AccountService) accountsrv:  AccountService,

    private toastr: ToastrService,
    private route: ActivatedRoute
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

  ngOnInit(): void {
    this.idSelectedInput = this.route.snapshot.paramMap.get("id");
    this.idSelectedInputNumber = (+ this.idSelectedInput);
    this.getItemById();
    this.ddlDataBinding();
  }

  getItemById() {
    this.service
      .apiSystemLogIdGet(this.idSelectedInputNumber)
      .subscribe((data) => {
        this.item = data;
      });
  }

  checkTheme() {
    this.themeService.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem("dark") == "true") {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }

  ddlDataBinding(): void {
        this.accountService.apiAccountGet().subscribe((result) => {
      this.accountItems = result;
    })

  }

  onUpdateItem() {
    /* OnUpdate
    this.service.apiSystemLogPut(this.item).subscribe(
      (data) => {
        this.toastr.success("Update successfully", "Notification");
      },
      (err) => {
        this.toastr.warning("Bad request", "Notification");
      }
    );
    OnUpdate */
  }
}
