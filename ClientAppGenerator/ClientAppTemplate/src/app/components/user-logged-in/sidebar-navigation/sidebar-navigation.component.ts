import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ThemeServiceService } from 'src/app/style-service/theme-service.service';
import { NavMenuItem } from 'src/models/nav-menu-item';
const listApi = require('../../../../../node_modules/@hqhoangvuong/api-client-803868/hqhoangvuong-api-client-803868.metadata.json');

@Component({
  selector: 'app-sidebar-navigation',
  templateUrl: './sidebar-navigation.component.html',
  styleUrls: ['./sidebar-navigation.component.scss'],
})

export class SidebarNavigationComponent implements OnInit {
  @Output() isChoosedEntity = new EventEmitter<boolean>();

  isDarkThemeSubscription: boolean = false;
  listNavMenuItems: NavMenuItem[] = [];
  excludeEntities: string[] = [
    'AuthService',
    'SystemDbSchemaService',
    'SystemMasterConfigService',
  ];

  hiddentEntities: string[] = [
    'AccountService',
    'BillService',
    'BillInfoService',
    'FoodService',
    'SystemLogService',
    'TableFoodService',
  ];

  constructor(private themeService: ThemeServiceService) {
    this.checkTheme();
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

  ngOnInit(): void {
    this.checkTheme();
    this.getAllServicesAsEntity();
  }

  getAllServicesAsEntity() {
    listApi.metadata.APIS.forEach((element: any) => {
      let idx: number = 0;
      if (!this.excludeEntities.some((x) => x === element.name) || !this.hiddentEntities.some((w) => w === element.name)) {
        let item = this.removeServiceInListEntity(element.name);
        let navItem: NavMenuItem = {
          id: idx,
          displayName: this.addSpaceEachChar(item),
          routingPath: item.toLowerCase(),
        };
        this.listNavMenuItems.push(navItem);
        idx += 1;
      }
    });
  }

  removeServiceInListEntity(item: any) {
    return item.replace('Service', 'Management');
  }
  
  addSpaceEachChar(item: any) {
    return item.replace(/([A-Z])/g, ' $1').trim();
  }

  closeNavDrawer() {
    this.isChoosedEntity.emit(true)
  }
}
