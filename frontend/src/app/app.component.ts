import { Component, AfterViewInit } from '@angular/core';
// import { FileUploader } from 'ng2-file-upload';
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';
import { ApiService } from './shared';

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
    fileId:string;
    filePath = '';
    postId: number;
    options: Object = {
        url: 'http://localhost:5000/upload',
        params: { 'post_id': this.postId }
    };

    constructor(
        private apiService: ApiService
    ) {
        console.log(apiService);
    }

    handleUpload(data): void {
        if (data && data.response) {
            data = JSON.parse(data.response);
            data = JSON.parse(data)
            this.fileId = data.id
            this.filePath = 'http://localhost:5000/file/'+data.filename;
            setTimeout(() => {
                this.activateAreaSelection()
            }, 200);
        }
    }

    ngAfterViewInit() {
    }

    sendCoors() {
        let vm = this;
        return function(c){
            console.log(c)
            let obj = {
                top: c.y,
                bottom: c.y2,
                left: c.x,
                right: c.x2
            };
            vm.apiService.mwPostJson('/coors/'+vm.fileId, obj).subscribe((data) => {
                console.log(data);
            });
        }
    }

    activateAreaSelection() {
        $('#input-image').Jcrop({
            onSelect: this.sendCoors()
        })
    }
}
