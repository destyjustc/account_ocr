import { Component, AfterViewInit, ApplicationRef} from '@angular/core';
// import { FileUploader } from 'ng2-file-upload';
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';
import { ApiService } from './shared';

declare var $;

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit{
    // public uploader:FileUploader = new FileUploader({url: URL});
    // public hasBaseDropZoneOver:boolean = false;
    fileId:string;
    filePath = '';
    postId: number;
    BASE_URL = '';
    options: Object;
    cropImg = []

    constructor(
        private apiService: ApiService,
        private applicationRef: ApplicationRef
    ) {
        this.BASE_URL = apiService.getBaseUrl();
        this.options = {
            url: this.BASE_URL+'/upload',
            params: { 'post_id': this.postId }
        };
    }

    handleUpload(data): void {
        if (data && data.response) {
            data = JSON.parse(data.response);
            data = JSON.parse(data)
            this.fileId = data.id
            this.filePath = this.BASE_URL+'/file/'+data.filename;
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
                data = JSON.parse(data)
                vm.cropImg.push(vm.BASE_URL+'/file/'+data.filename);
                console.log(vm.cropImg);
                vm.applicationRef.tick();
            });
        }
    }

    activateAreaSelection() {
        $('#input-image').Jcrop({
            onSelect: this.sendCoors()
        })
    }
}
