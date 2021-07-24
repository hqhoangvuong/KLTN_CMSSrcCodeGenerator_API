import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TableFoodService, TableFood } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "app-tablefood-read-ui-component",
  templateUrl: "./tablefood-read-ui.component.html",
  styleUrls: ["./tablefood-read-ui.component.scss"],
})

export class TableFoodReadUIComponent implements OnInit {
  service: TableFoodService;
  isDarkThemeSubscription: boolean=false;
  item: TableFood;
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject(TableFoodService) srv: TableFoodService,
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
    this.service.apiTableFoodIdGet(this.idSelectedInputNumber).subscribe(data => {
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
