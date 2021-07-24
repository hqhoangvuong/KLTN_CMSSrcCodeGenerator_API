import { Component, Inject, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';
import { FoodService, Food,   } from '@hqhoangvuong/api-client-803868';
import { HttpHeaders } from "@angular/common/http";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-food-create-ui-component",
  templateUrl: "./food-create-ui.component.html",
  styleUrls: ["./food-create-ui.component.scss"],
})

export class FoodcreateUIComponent implements OnInit {
  isDarkThemeSubscription: boolean = false;
  entityDisplayName = "Create";
  isContinueToCreate: boolean = true;
  service: FoodService;
  item: Food;


  itemSeleted: any;
  token: any;

  constructor(
    private themeSerive: ThemeServiceService,
    private route: Router,
    @Inject(FoodService) srv: FoodService,

    private toast: ToastrService
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as Food;
    this.service = srv;

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

  }

  createNewItem() {
    this.service.apiFoodPost(this.item).subscribe(
      (data) => {
        this.toast.success("Create new Foody successfully", "Information");
      },
      (err) => {
        this.toast.warning("Something wrong happen", "Warning");
      }
    );

    if (!this.isContinueToCreate) {
      this.route.navigate(['/user/index/foodmanagement']);
    }
  }
}
