import { Component, AfterViewInit } from '@angular/core';
// import { FileUploader } from 'ng2-file-upload';
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';

declare var $;

const URL = 'http://localhost:5000/upload';
@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit{
    // public uploader:FileUploader = new FileUploader({url: URL});
    // public hasBaseDropZoneOver:boolean = false;
    filePath = '';
    postId: number;
    options: Object = {
        url: 'http://localhost:5000/upload',
        params: { 'post_id': this.postId }
    };

    handleUpload(data): void {
        if (data && data.response) {
            data = JSON.parse(data.response);
            data = JSON.parse(data)
            this.filePath = 'http://localhost:5000/file/'+data.filename;
            setTimeout(() => {
                this.activateAreaSelection()
            }, 200);
        }
    }

    ngAfterViewInit() {
    }

    sendCoors(c) {
        console.log(c)
    }

    activateAreaSelection() {
        $('#input-image').Jcrop({
            onSelect: this.sendCoors
        })
    }
}
