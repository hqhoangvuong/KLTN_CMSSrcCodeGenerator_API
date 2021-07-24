import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateUIComponent } from './update-ui.component';

describe('UpdateUIComponent', () => {
  let component: UpdateUIComponent;
  let fixture: ComponentFixture<UpdateUIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateUIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateUIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
