<template>
<div>
    <a class="btn btn-primary download" @click="download_pdf" v-if="loading == false">Download PDF</a>
    <div id="report1">
        <div v-if="loading" class="loader">
            <svg width="200px" height="200px"  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" style="background: none;">
                <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.875s"></animate>
                </circle>
                <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.75s"></animate>
                </circle>
                <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.625s"></animate>
                </circle>
                <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.5s"></animate>
                </circle>
                <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.375s"></animate>
                </circle>
                <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.25s"></animate>
                </circle>
                <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="-0.125s"></animate>
                </circle>
                <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate attributeName="r" values="4.8;4.8;8;4.8;4.8" times="0;0.1;0.2;0.3;1" dur="1s" repeatCount="indefinite" begin="0s"></animate>
                </circle>
            </svg>
        </div> 
        <div v-else>
            <div class="col-md-12 main-div">
                <div class="main-heading heading-111">
                    <h1> VELOX.HORSE</h1>
                </div>
                <div class="heading">
                    <h1> DNA + CARDIO + BIOMECHANICS REPORT</h1>
                </div>
                <div class="horse_detail matrix">
                    <h5>HORSE DETAILS</h5>
                    <ul>
                        <li>NAME: {{result.name ? result.name : '-'}}</li>
                        <li>SEX: {{result.sex ? result.sex : '-'}}</li>
                        <li>DOB: {{result.date_of_birth ? result.date_of_birth : '-'}}</li>
                        <li>SIRE: {{result.sire ? result.sire : '-'}}</li>
                        <li>DAM: {{result.dam ? result.dam : '-'}}</li>
                        <li>BROODMARE SIRE: {{result.broodmare_sire ? result.broodmare_sire : '-'}}</li>
                        <li>TYPE: {{result.type ? result.type : '-'}}</li>
                        <li>STATUS: {{result.status ? result.status : '-'}}</li>
                        <li>DATE OF MEASURE: {{date_of_measure ? date_of_measure : '-'}}</li>
                        <li>MEASUREMENT TYPE: {{measure_type ? measure_type : '-'}}</li>
                    </ul>
                    <table class="table table-bordered responsive">
                        <tbody>
                            <tr>
                                <td width="30%" class="text-center"><img src="../../assets/img/icon-1.png"></td> 
                                <td style="font-size: 18px; vertical-align: middle;">DNA+Cardio+Biomechanics Score : {{prob_cardio_bio_model_score ? prob_cardio_bio_model_score : 'Not Available'}}</td>
                            </tr> 
                            <tr>
                                <td width="30%" class="text-center"><img src="../../assets/img/icon-2.png"></td> 
                                <td style="font-size: 18px; vertical-align: middle;">BIOMECHANICS SCORE : {{prob_bio_model_score ? prob_bio_model_score : 'Not Available'}}</td>
                            </tr> 
                            <tr>
                                <td width="30%" class="text-center"><img src="../../assets/img/icon-3.png"></td> 
                                <td style="font-size: 18px; vertical-align: middle; line-height: 50px;">CARDIO SHAPE : {{cardio_type ? cardio_type : 'Not Available'}}<br>
                                    CARDIO QUALITY SCORE : {{cardio_video_score ? cardio_video_score : 'Not Available'}}
                                </td>
                            </tr>
                            <tr>
                                <td width="30%" class="text-center"><img src="../../assets/img/icon-4.png"></td>
                                 <td style="font-size: 18px; vertical-align: middle; line-height: 50px;">OPTIMAL DISTANCE : {{result.pred_opt_dist ? result.pred_opt_dist : 'Not Available'}}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="col-md-12 div2">
                <div class="chart">
                    <h1>DNA + Cardio + Biomechanics - Current Model Performance</h1>
                    <div class="row">
                        <div class="col-md-5">
                            <canvas id="myChart11"></canvas>
                        </div>
                         <div class="col-md-5">
                            <table class="table table-borderless percantage_all">
                                <thead>
                                    <tr>
                                    <th scope="col">Horse Rating</th>
                                    <th scope="col">{{prob_cardio_bio_model_score ? prob_cardio_bio_model_score : 'Not Available'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of All</th>
                                    <th scope="col" v-for="per ,index_2 in  percentageArrAll" :key="index_2">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite in Group</th>
                                    <th scope="col" v-for="per ,index_3 in  percentageArrElite" :key="index_3">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite of all Elite</th>
                                    <th scope="col" v-for="per ,index_4 in  percentageArrEliteofElite" :key="index_4">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">Odds Ratio</th>
                                    <th scope="col" v-for="per ,index_5 in  ratio" :key="index_5">{{per.percentage}}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                         </div>
                    </div>
                </div>
                <div class="chart">
                    <h1>Biomechanics - Current Model Performance</h1>
                    <div class="row">
                        <div class="col-md-5">
                            <canvas id="myChart22"></canvas>
                        </div>
                        <div class="col-md-5">
                            <table class="table table-borderless percantage_all">
                                <thead>
                                    <tr>
                                    <th scope="col">Horse Rating</th>
                                    <th scope="col">{{prob_bio_model_score ? prob_bio_model_score : 'Not Available'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of All</th>
                                    <th scope="col" v-for="per ,index_2 in  biomechanics_percentageArrAll" :key="index_2">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite in Group</th>
                                    <th scope="col" v-for="per ,index_3 in  biomechanics_percentageArrElite" :key="index_3">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite of all Elite</th>
                                    <th scope="col" v-for="per ,index_4 in  biomechanics_percentageArrEliteofElite" :key="index_4">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">Odds Ratio</th>
                                    <th scope="col" v-for="per ,index_5 in  biomechanics_ratio" :key="index_5">{{per.percentage}}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="chart">
                    <h1>Cardio - Current Model Performance</h1>
                    <div class="row">
                        <div class="col-md-5">
                            <canvas id="myChart33"></canvas>
                        </div>
                        <div class="col-md-5">
                            <table class="table table-borderless percantage_all">
                                <thead>
                                    <tr>
                                    <th scope="col">Horse Rating</th>
                                    <th scope="col">{{cardio_video_score ? cardio_video_score : 'Not Available'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of All</th>
                                    <th scope="col" v-for="per ,index_2 in  cardio_percentageArrAll" :key="index_2">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite in Group</th>
                                    <th scope="col" v-for="per ,index_3 in  cardio_percentageArrElite" :key="index_3">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">% of Elite of all Elite</th>
                                    <th scope="col" v-for="per ,index_4 in  cardio_percentageArrEliteofElite" :key="index_4">{{per.percentage+'%'}}</th>
                                    </tr>
                                    <tr>
                                    <th scope="col">Odds Ratio</th>
                                    <th scope="col" v-for="per ,index_5 in  cardio_ratio" :key="index_5">{{per.percentage}}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <p class="footer_text" id="footer_text"><span>DISCLAIMER:</span> This is a predictive test, not a diagnostic test. In no way is this test representing or making claim to any disease state
                    in the thoroughbred, not are any agents or employees of Performance Genetics asserting any claims in regards to a disease state in
                    the thoroughbred.</p>
            </div>
        </div>   
    </div>
</div>
</template>

<script>
import Chart from "chart.js";
import api from "@/services/axios";
import {DNACardioBiomechanicsScoreByAge} from '@/js/DNACardioBiomechanicsScoreByAge.js'
import {BiomechanicsScoreByAge} from '@/js/BiomechanicsScoreByAge.js'
import { CardioScoreByAge } from "@/js/CardioScoreByAge.js";

export default {
    name:"CardioBioReport",
    data(){
        return {
            result:[],
            loading: false,
            date_of_measure:'',
            measure_type:'',
            prob_cardio_bio_model_score:'',
            prob_bio_model_score:'',
            cardio_type:'',
            cardio_video_score:'',
            DNACardioBiomechanicsScoreByAge: DNACardioBiomechanicsScoreByAge,
            BiomechanicsScoreByAge: BiomechanicsScoreByAge,
            CardioScoreByAge: CardioScoreByAge,
            measure_id: '',
            temp10:[],
            temp11:[],
            temp12:[],
            sum:"",
            sum1:'',
            sum2:'',
            percentageArrAll:[],
            percentageArrElite:[],
            percentageArrEliteofElite:[],
            ratio:[],
            biomechanics_percentageArrAll:[],
            biomechanics_percentageArrElite:[],
            biomechanics_percentageArrEliteofElite:[],
            biomechanics_ratio:[],
            cardio_percentageArrAll:[],
            cardio_percentageArrElite:[],
            cardio_percentageArrEliteofElite:[],
            cardio_ratio:[]
        }
    },
    async mounted()
    {
        let temp1=[];
        this.loading = true
        let url = window.location.href;
        this.measure_id = url.split("/");
        api.get(`/horses/${this.$route.params.id}/`)
            .then(async response=>{
               this.result = response.data
               temp1= this.result.measures.filter(item => item.id == this.measure_id[7]),
               this.date_of_measure=temp1[0]['date_of_measure']
               this.measure_type = temp1[0]['measure_type']
               this.prob_cardio_bio_model_score = temp1[0]['prob_cardio_bio_model_score']
               this.prob_bio_model_score = temp1[0]['prob_bio_model_score']
               this.cardio_type = temp1[0]['cardio_type']
               this.cardio_video_score = temp1[0]['cardio_video_score']

                setTimeout(()=>{this.loading = false},12000)
                setTimeout(()=>{this.chart()},0)
            })
            .catch(error=>{ })
    },
    methods: 
    {
        download_pdf() 
        {
            const options = {
                margin: 0.1,
                filename: 'DNA + Cardio + Bio Report.pdf',
                image: { 
                    type: 'PNG', 
                    quality: 1 
                },
                html2canvas: { 
                    useCORS: true,
                },
                jsPDF: { 
                    unit: 'in', 
                    format: 'letter', 
                    orientation: 'portrait' 
                }
            }
            const element = document.getElementById('report1');
            html2pdf().from(element).set(options).save();
        },
        chart()
        {
            let temp,data = [];
            let temp1,data1 = [];
            let temp2,data2 = [];
            api.get(`/horses/stats/`)
            .then(response => { 
                temp = response.data?.dna_cardio_biomechanics?.age; 
                this.temp10 = response.data?.dna_cardio_biomechanics?.age.map(item => item.counts);
                if (this.temp10 != undefined) {
                    this.sum = this.temp10.reduce((partialSum, a) => partialSum + a, 0);
                }
                temp.forEach((element) => {
                     data.push({
                        horse_type: element.horse_type,
                        score: element.score,
                        elite: element.elite,
                        counts: element.counts,
                    });
                });
                const ctx1 = document.getElementById("myChart11");
                if (window.bar18 != undefined) 
                {
                    window.bar18.destroy();
                }
                const chart_type_data =this.DNACardioBiomechanicsScoreByAge(data)
                this.getPercentage(chart_type_data)
                window.bar18 = new Chart(ctx1, chart_type_data);

                temp1 = response.data?.biomechanics?.age;
                this.temp11 = response.data?.biomechanics?.age.map(item => item.counts);
                if (this.temp11 != undefined) {
                    this.sum1 = this.temp11.reduce((partialSum, a) => partialSum + a, 0);
                }
                temp1.forEach((element) => {
                    data1.push({
                        horse_type: element.horse_type,
                        score: element.score,
                        elite: element.elite,
                        counts: element.counts,
                    });
                });

                const ctx2 = document.getElementById("myChart22");
                if (window.bar19 != undefined) 
                {
                    window.bar19.destroy();
                }
                const chart_type_data2 =this.BiomechanicsScoreByAge(data1)
                this.getPercentage2(chart_type_data2)
                window.bar19 = new Chart(ctx2, chart_type_data2);

                temp2 = response.data?.cardio?.age;
                this.temp12 = response.data?.cardio?.age.map(item => item.counts);
                if (this.temp12 != undefined) {
                    this.sum2 = this.temp12.reduce((partialSum, a) => partialSum + a, 0);
                }

                temp2.forEach((element) => {
                    data2.push({
                        horse_type: element.horse_type,
                        score: element.score,
                        elite: element.elite,
                        counts: element.counts,
                    });
                });

                const ctx3 = document.getElementById("myChart33");
                if (window.bar20 != undefined) 
                {
                    window.bar20.destroy();
                }
                const chart_type_data3 =this.CardioScoreByAge(data2)
                this.getPercentage3(chart_type_data3)
                window.bar20 = new Chart(ctx3, chart_type_data3);
            })
        },
        async getPercentage(chartData){
            this.percentageArrAll = []
            this.percentageArrElite = []
            this.percentageArrEliteofElite=[]
            this.ratio=[]
            const label = this.prob_cardio_bio_model_score

            /* calculate for step 1 start*/
            const labelViseArr = chartData.filteredArrData.filter(x => x.score == label)
            const labelSum = labelViseArr.reduce((partialSum, a) => partialSum + a.sum, 0);
            const percentage = ((labelSum*100)/this.sum).toFixed(2);
            this.percentageArrAll.push({score:label, percentage:percentage})
            /* calculate for step 1 end*/

            /* calculate for step 2 start*/
            const labelViseArr1 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const labelSum1 = labelViseArr1.reduce((partialSum, a) => partialSum + a.sum, 0);
            const labelViseArr2 = chartData.filteredArrData.filter(x => x.score == label)
            const labelSum2 = labelViseArr2.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(labelSum1 != 0 || labelSum2 != 0){
                var percentage1 =((labelSum1*100)/labelSum2).toFixed(2);
            }
            else{
                var percentage1 = 0
            }
            this.percentageArrElite.push({score:label, percentage:percentage1})
            /* calculate for step 2 end*/

            /* calculate for step 3 start*/
            const labelViseArr3 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const labelSum5 = labelViseArr3.reduce((partialSum, a) => partialSum + a.sum, 0);
            const labelViseArr6 = chartData.filteredArrData.filter(x => x.elite=='Yes')
            const labelSum6 = labelViseArr6.reduce((partialSum, a) => partialSum + a.sum, 0);
            const percentage3 = ((labelSum5*100)/labelSum6).toFixed(2);
            this.percentageArrEliteofElite.push({score:label, percentage:percentage3})
            /* calculate for step 3 end*/  

            /* calculate for step 4 start*/
            const labelViseArr4 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const labelSum3 = labelViseArr4.reduce((partialSum, a) => partialSum + a.sum, 0);
            const labelViseArr5 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='No')
            const labelSum4 = labelViseArr5.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(labelSum3 == 0 || labelSum4 == 0 || labelSum3 == "" || labelSum4 == "" || isNaN(labelSum3) || isNaN(labelSum4)){
                var percentage2 = 0;
            }
            else{
                var percentage2 = ((labelSum3/labelSum4) / (labelSum4/labelSum3)).toFixed(2);
            }
            this.ratio.push({score:label, percentage:percentage2})
            /* calculate for step 4 end*/
                
        },
        async getPercentage2(chartData){
            this.biomechanics_percentageArrAll = []
            this.biomechanics_percentageArrElite = []
            this.biomechanics_percentageArrEliteofElite=[]
            this.biomechanics_ratio=[]
            
            const label = this.prob_bio_model_score

            /* calculate for step 1 start*/
            const biomechanics_labelViseArr = chartData.filteredArrData.filter(x => x.score == label)
            const biomechanics_labelSum = biomechanics_labelViseArr.reduce((partialSum, a) => partialSum + a.sum, 0);
            const biomechanics_percentage = ((biomechanics_labelSum*100)/this.sum1).toFixed(2);
            this.biomechanics_percentageArrAll.push({score:label, percentage:biomechanics_percentage})
            /* calculate for step 1 end*/

            /* calculate for step 2 start*/
            const biomechanics_labelViseArr1 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const biomechanics_labelSum1 = biomechanics_labelViseArr1.reduce((partialSum, a) => partialSum + a.sum, 0);
            const biomechanics_labelViseArr2 = chartData.filteredArrData.filter(x => x.score == label)
            const biomechanics_labelSum2 = biomechanics_labelViseArr2.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(biomechanics_labelSum1 != 0 || biomechanics_labelSum2 != 0){
                var biomechanics_percentage1 =((biomechanics_labelSum1*100)/biomechanics_labelSum2).toFixed(2);
            }
            else{
                var biomechanics_percentage1 = 0
            }
            this.biomechanics_percentageArrElite.push({score:label, percentage:biomechanics_percentage1})
            /* calculate for step 2 end*/

            /* calculate for step 3 start*/
            const biomechanics_labelViseArr3 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const biomechanics_labelSum5 = biomechanics_labelViseArr3.reduce((partialSum, a) => partialSum + a.sum, 0);
            const biomechanics_labelViseArr6 = chartData.filteredArrData.filter(x => x.elite=='Yes')
            const biomechanics_labelSum6 = biomechanics_labelViseArr6.reduce((partialSum, a) => partialSum + a.sum, 0);
            const biomechanics_percentage3 = ((biomechanics_labelSum5*100)/biomechanics_labelSum6).toFixed(2);
            this.biomechanics_percentageArrEliteofElite.push({score:label, percentage:biomechanics_percentage3})
            /* calculate for step 3 end*/  

            /* calculate for step 4 start*/
            const biomechanics_labelViseArr4 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const biomechanics_labelSum3 = biomechanics_labelViseArr4.reduce((partialSum, a) => partialSum + a.sum, 0);
            const biomechanics_labelViseArr5 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='No')
            const biomechanics_labelSum4 = biomechanics_labelViseArr5.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(biomechanics_labelSum3 == 0 || biomechanics_labelSum4 == 0 || biomechanics_labelSum3 == "" || biomechanics_labelSum4 == "" || isNaN(biomechanics_labelSum3) || isNaN(biomechanics_labelSum4)){
                var biomechanics_percentage2 = 0;
            }
            else{
                var biomechanics_percentage2 = ((biomechanics_labelSum3/biomechanics_labelSum4) / (biomechanics_labelSum4/biomechanics_labelSum3)).toFixed(2);
            }
            this.biomechanics_ratio.push({score:label, percentage:biomechanics_percentage2})
            /* calculate for step 4 end*/
        },
        async getPercentage3(chartData){
            this.cardio_percentageArrAll = []
            this.cardio_percentageArrElite = []
            this.cardio_percentageArrEliteofElite=[]
            this.cardio_ratio=[]
            
            const label = this.cardio_video_score

            /* calculate for step 1 start*/
            const cardio_labelViseArr = chartData.filteredArrData.filter(x => x.score == label)
            const cardio_labelSum = cardio_labelViseArr.reduce((partialSum, a) => partialSum + a.sum, 0);
            const cardio_percentage = ((cardio_labelSum*100)/this.sum2).toFixed(2);
            this.cardio_percentageArrAll.push({score:label, percentage:cardio_percentage})
            /* calculate for step 1 end*/

            /* calculate for step 2 start*/
            const cardio_labelViseArr1 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const cardio_labelSum1 = cardio_labelViseArr1.reduce((partialSum, a) => partialSum + a.sum, 0);
            const cardio_labelViseArr2 = chartData.filteredArrData.filter(x => x.score == label)
            const cardio_labelSum2 = cardio_labelViseArr2.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(cardio_labelSum1 != 0 || cardio_labelSum2 != 0){
                var cardio_percentage1 =((cardio_labelSum1*100)/cardio_labelSum2).toFixed(2);
            }
            else{
                var cardio_percentage1 = 0
            }
            this.cardio_percentageArrElite.push({score:label, percentage:cardio_percentage1})
            /* calculate for step 2 end*/

            /* calculate for step 3 start*/
            const cardio_labelViseArr3 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const cardio_labelSum5 = cardio_labelViseArr3.reduce((partialSum, a) => partialSum + a.sum, 0);
            const cardio_labelViseArr6 = chartData.filteredArrData.filter(x => x.elite=='Yes')
            const cardio_labelSum6 = cardio_labelViseArr6.reduce((partialSum, a) => partialSum + a.sum, 0);
            const cardio_percentage3 = ((cardio_labelSum5*100)/cardio_labelSum6).toFixed(2);
            this.cardio_percentageArrEliteofElite.push({score:label, percentage:cardio_percentage3})
            /* calculate for step 3 end*/

            /* calculate for step 4 start*/
            const cardio_labelViseArr4 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='Yes')
            const cardio_labelSum3 = cardio_labelViseArr4.reduce((partialSum, a) => partialSum + a.sum, 0);
            const cardio_labelViseArr5 = chartData.filteredArrData.filter(x => x.score == label && x.elite=='No')
            const cardio_labelSum4 = cardio_labelViseArr5.reduce((partialSum, a) => partialSum + a.sum, 0);
            if(cardio_labelSum3 == 0 || cardio_labelSum4 == 0 || cardio_labelSum3 == "" || cardio_labelSum4 == "" || isNaN(cardio_labelSum3) || isNaN(cardio_labelSum4)){
                var cardio_percentage2 = 0;
            }
            else{
                var cardio_percentage2 = ((cardio_labelSum3/cardio_labelSum4) / (cardio_labelSum4/cardio_labelSum3)).toFixed(2);
            }
            this.cardio_ratio.push({score:label, percentage:cardio_percentage2})
            /* calculate for step 4 end*/
        },
    },
}
</script>
<style>
.main-div {
    width: 100%;
    border: 1px solid;
    border-radius: 20px;
    height: 1030px;
}
.main-heading {
    text-align: center;
    padding: 7px;
    width: 100%;
    border-bottom: 0;
}
.heading-111 {
    text-align: center;
}
.heading-111 h1 {
    font-size: 25px;
    margin-top: 10px;
}
.heading {
    text-align: center;
    border: 1px solid;
    padding: 10px;
    width: 100%;
    background-color: #bbdeea;
}
.heading h1 {
    font-size: 21px;
    margin: 0px;
}
.horse_detail h5 {
    font-size: 19px;
    font-weight: bolder;
    margin-bottom: 20px;
    margin-top: 20px;
}
.horse_detail ul {
    list-style: none;
    margin: 0;
    padding: 0;
}
.horse_detail ul li {
    font-size: 18px;
    margin-bottom: 10px;
}
.matrix .table-bordered {
    border: 5px solid #dee2e6;
    margin-top: 10px;
}
.matrix .table th, .table td {
    vertical-align: top;
}
.matrix .table-bordered th, .table-bordered td {
    border: 5px solid #dee2e6 !important;
    padding: 7px .75rem !important;
}
.chart h1 {
    font-size: 18px;
    margin-top: 10px;
}
.div2 {
    margin-top: 10px;
    width: 100%;
    border: 1px solid;
    border-radius: 20px;
}
p.footer_text {
    font-size: 17px;
    line-height: 20px;
    margin-top: 10px;
    text-align: justify;
}
.footer_text span {
    font-weight: bold;
}
a.download {
    cursor: pointer;
    color: white !important;
    margin-bottom: 10px;
}
.loader {
    text-align: center;
}
/* .percantage_all th:first-child {
  width: 25%;
} */
.percantage_all th {
    width: 13%;
    font-size: 12.8px;
    text-align: left !important;
    padding-left: 0px;
    padding-right: 0px;
    font-weight: 400;
    line-height: 12px;
}
table.percantage_all {
    width: 70%;
    margin-left: 220px;
}
</style>