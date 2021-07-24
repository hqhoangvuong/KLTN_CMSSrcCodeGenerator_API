import { Component, Inject, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';
import { BillService, Bill, TableFoodService,  TableFood,  } from '@hqhoangvuong/api-client-803868';
import { HttpHeaders } from "@angular/common/http";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-bill-create-ui-component",
  templateUrl: "./bill-create-ui.component.html",
  styleUrls: ["./bill-create-ui.component.scss"],
})

export class BillcreateUIComponent implements OnInit {
  isDarkThemeSubscription: boolean = false;
  entityDisplayName = "Create";
  isContinueToCreate: boolean = true;
  service: BillService;
  item: Bill;
  tableFoodItems: TableFood[] = [];

  tableFoodService: TableFoodService;

  itemSeleted: any;
  token: any;

  constructor(
    private themeSerive: ThemeServiceService,
    private route: Router,
    @Inject(BillService) srv: BillService,
    @Inject(TableFoodService) tableFoodsrv:  TableFoodService,

    private toast: ToastrService
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
    tableFoodsrv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as Bill;
    this.service = srv;
    this.tableFoodService = tableFoodsrv;

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
    this.tableFoodService.apiTableFoodGet().subscribe((result) => {
      this.tableFoodItems = result;
    })

  }

  createNewItem() {
    /* CreateLogicSession
    this.service.apiBillPost(this.item).subscribe(
      (data) => {
        this.toast.success("Create new Bill Information Management successfully", "Information");
      },
      (err) => {
        this.toast.warning("Something wrong happen", "Warning");
      }
    );

    if (!this.isContinueToCreate) {
      this.route.navigate(['/user/index/billmanagement']);
    }
    CreateLogicSession */
  }
}
