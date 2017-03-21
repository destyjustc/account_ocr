import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { IndexPageComponent } from './index-page/index-page.component';
import { FileSelectDirective, FileDropDirective } from 'ng2-file-upload'; 
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';
import {Ng2PaginationModule} from 'ng2-pagination';

import { ApiService } from './shared';

@NgModule({
  declarations: [
    AppComponent,
    IndexPageComponent,
    UPLOAD_DIRECTIVES
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    Ng2PaginationModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
