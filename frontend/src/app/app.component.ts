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

    zoom = 1;

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
                let obj = {
                    img: vm.BASE_URL+'/file/'+data.filename,
                    positions: data.locations,
                    results: data.results
                };
                vm.cropImg.push(obj);
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

    getResultItemStyle(p) {
        return {
            'position': 'relative',
            'top': p[0]+'px',
            'line-height': (p[1]-p[0])*this.zoom+'px',
            'left':'0px'
        };
    }

    getResultImageStyle(obj) {
        console.log(obj);
        if (obj.positions.length) {
            let diff = obj.positions[0][1]-obj.positions[0][0];
            this.zoom = Math.floor(30/diff);
            let height = (100*this.zoom).toString()+'%';
            return {
                '-moz-transform': 'scale('+this.zoom+')',
                '-webkit-transform': 'scale('+this.zoom+')',
                'transform': 'scale('+this.zoom+')'
            }
        }
    }

    onSubmit() {
        console.log(this.cropImg);
    }
}
