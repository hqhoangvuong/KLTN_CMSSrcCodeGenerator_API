import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MaterialModule } from './material.module';
import { IndexUIComponent } from './components/user-logged-in/index-ui.component';
import { SidebarNavigationComponent } from './components/user-logged-in/sidebar-navigation/sidebar-navigation.component';
import { SearchUIComponent } from './components/user-logged-in/search-ui/search-ui.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ApiModule, BASE_PATH } from '@hqhoangvuong/api-client-803868';
import { HttpClientModule } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { RouterModule } from '@angular/router';
import { ToastrModule } from 'ngx-toastr';
import { LoginScreenComponent } from './components/login-screen/login-screen.component';
import { LoginContentComponent } from './components/login-screen/login-content/login-content.component';
import { RegisterContentComponent } from './components/login-screen/register-content/register-content.component';
import { NotFoundComponent } from './components/commons/not-found/not-found.component';
import { UserInformationComponent } from './components/user-logged-in/user-information/user-information.component';
import { FooterComponent } from './components/user-logged-in/footer/footer.component';
import { AccountTableUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui.component';
import { BillTableUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui.component';
import { BillInfoTableUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui.component';
import { FoodTableUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui.component';
import { SystemLogTableUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui.component';
import { TableFoodTableUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui.component';

/** ImportComponentForAction. */
import { AccountUpdateUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-update-ui-component/account-update-ui.component';
import { BillUpdateUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-update-ui-component/bill-update-ui.component';
import { BillInfoUpdateUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-update-ui-component/billinfo-update-ui.component';
import { FoodUpdateUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-update-ui-component/food-update-ui.component';
import { SystemLogUpdateUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-update-ui-component/systemlog-update-ui.component';
import { TableFoodUpdateUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-update-ui-component/tablefood-update-ui.component';
import { AccountcreateUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-create-ui-component/account-create-ui.component';
import { BillcreateUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-create-ui-component/bill-create-ui.component';
import { BillInfocreateUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-create-ui-component/billinfo-create-ui.component';
import { FoodcreateUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-create-ui-component/food-create-ui.component';
import { SystemLogcreateUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-create-ui-component/systemlog-create-ui.component';
import { TableFoodcreateUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-create-ui-component/tablefood-create-ui.component';
import { AccountReadUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-read-ui-component/account-read-ui.component';
import { BillReadUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-read-ui-component/bill-read-ui.component';
import { BillInfoReadUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-read-ui-component/billinfo-read-ui.component';
import { FoodReadUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-read-ui-component/food-read-ui.component';
import { SystemLogReadUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-read-ui-component/systemlog-read-ui.component';
import { TableFoodReadUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-read-ui-component/tablefood-read-ui.component';
import { AccountDeleteUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-delete-ui-dialog/account-delete-ui-dialog.component';
import { BillDeleteUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-delete-ui-dialog/bill-delete-ui-dialog.component';
import { TableFoodDeleteUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-delete-ui-dialog/tablefood-delete-ui-dialog.component';
@NgModule({
  declarations: [
    AppComponent,
    IndexUIComponent,
    SidebarNavigationComponent,
    SearchUIComponent,
    LoginScreenComponent,
    LoginContentComponent,
    RegisterContentComponent,
    NotFoundComponent,
    UserInformationComponent,
    FooterComponent,
    AccountTableUIComponent,
    BillTableUIComponent,
    BillInfoTableUIComponent,
    FoodTableUIComponent,
    SystemLogTableUIComponent,
    TableFoodTableUIComponent,

/** DeclareComponentForAction. */
    AccountUpdateUIComponent,
    BillUpdateUIComponent,
    BillInfoUpdateUIComponent,
    FoodUpdateUIComponent,
    SystemLogUpdateUIComponent,
    TableFoodUpdateUIComponent,
    AccountcreateUIComponent,
    BillcreateUIComponent,
    BillInfocreateUIComponent,
    FoodcreateUIComponent,
    SystemLogcreateUIComponent,
    TableFoodcreateUIComponent,
    AccountReadUIComponent,
    BillReadUIComponent,
    BillInfoReadUIComponent,
    FoodReadUIComponent,
    SystemLogReadUIComponent,
    TableFoodReadUIComponent,
    AccountDeleteUIComponent,
    BillDeleteUIComponent,
    TableFoodDeleteUIComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    RouterModule,
    BrowserAnimationsModule,
    ApiModule,
    HttpClientModule,
    FontAwesomeModule,
    ToastrModule.forRoot({
      timeOut: 1000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    }),
  ],
  providers: [{ provide: BASE_PATH, useValue: environment.API_BASE_PATH }],
  bootstrap: [AppComponent],
})
export class AppModule {}
