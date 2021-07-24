import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FoodService, Food } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "app-food-read-ui-component",
  templateUrl: "./food-read-ui.component.html",
  styleUrls: ["./food-read-ui.component.scss"],
})

export class FoodReadUIComponent implements OnInit {
  service: FoodService;
  isDarkThemeSubscription: boolean=false;
  item: Food;
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject(FoodService) srv: FoodService,
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
    this.service.apiFoodIdGet(this.idSelectedInputNumber).subscribe(data => {
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
