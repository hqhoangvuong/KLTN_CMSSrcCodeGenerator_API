import {
  Component,
  OnInit,
  Output,
  EventEmitter,
  HostListener,
  Inject,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';
import { ThemeServiceService } from '../../../style-service/theme-service.service';
import { TableFoodDeleteUIComponent } from './tablefood-table-ui-action/tablefood-delete-ui-dialog/tablefood-delete-ui-dialog.component';
import { ToastrService } from 'ngx-toastr';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { TableFoodService, TableFood } from '@hqhoangvuong/api-client-803868';

@Component({
  selector: 'app-tablefood-table-ui',
  templateUrl: './tablefood-table-ui.component.html',
  styleUrls: ['./tablefood-table-ui.component.scss'],
})

export class TableFoodTableUIComponent implements OnInit {
  _service: TableFoodService;
  modelDisplayName: string;
  listItems: TableFood[] = [];
  @Output() nameActionTrigger = new EventEmitter<any>();
  contentType: string[] = ['text/html', 'charset=UTF-8'];
  pageIndex: number = 1;
  pageSize: number = 10;
  pageDataTotalCount: number;
  pageEvent: PageEvent;
  map: { [key: string]: string } = {};
  string: [] = [];
  token: any;
  httpClient: HttpClient;
  isDarkThemeSubscription: boolean = false;
  isFiltering: boolean=false;
  filterKey: string= ''

  constructor(
    private themeService: ThemeServiceService,
    public dialog: MatDialog,
    private toastr: ToastrService,
    @Inject(TableFoodService) _service: TableFoodService
  ) {
    this.checkTheme();
    this.token = localStorage.getItem('accessToken');
    _service.defaultHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ` + this.token,
    });
    this._service = _service;
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
    this.getPagingApi(this.pageIndex, this.pageSize);
    this.getAllApi();
  }

  getPagingApi(pageIndex: number, pageSize: number) {
    this._service
      .apiTableFoodPagingGet(pageIndex, pageSize)
      .subscribe((result) => {
        this.listItems = result;
      });
  }

  getAllApi() {
    this._service.apiTableFoodPagingGet(0, 10).subscribe((result) => {
      this.pageDataTotalCount = Object.keys(result).length;
    });
  }

  onClickEdit(id: any) {
    this.nameActionTrigger.emit({ type: 'edit', idItem: id });
  }

  reGetPagingData() {
    this.getPagingApi(this.pageIndex, this.pageSize);
  }

  gotoPrevious() {
    var sizePrevious = 0;
    sizePrevious = this.pageSize - 10;
    if (sizePrevious > 0) {
      this.pageSize = sizePrevious;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  gotoNext() {
    var sizeNext = 0;
    sizeNext =+ this.pageSize + +10;
    if (sizeNext > 0) {
      this.pageSize = sizeNext;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  onClickDelete(id: any) {
    const dialogRef = this.dialog.open(TableFoodDeleteUIComponent, {
      data: { idSelected: id },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result.data) {
        this._service.apiTableFoodDelete(id).subscribe(
          (res) => {
            this.toastr.success("Delete successfully", "Notification");
            this.getPagingApi(this.pageIndex, this.pageSize);
            this.getAllApi();
          },
          (err) => {
            if (err.status === 400) {
              this.toastr.warning(err.error, 'Warning');
            }
          }
        );
      }
    });
  }

  onClickView(id: any) {
    this.nameActionTrigger.emit({ type: 'read', idItem: id });
  }

  async applyFilter(event: any) {
    if (this.filterKey === '' ) {
      this.ngOnInit();
    } else if (event.code === 'Backspace') {
      this.ngOnInit();
      this.listItems = this.listItems.filter(item => {
        return ("" + item.id).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
    } else{
      this.listItems = this.listItems.filter(item => {
        return ("" + item.id).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
   }
  }
}

export interface DialogData {
  idSelected: any;
}
