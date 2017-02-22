import { Component, AfterViewInit } from '@angular/core';

declare var $;

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit{
    title = 'app works!';

    ngAfterViewInit() {
        console.log($)
    }
}
