def grafico_hombres_vs_mujeres(total_patients, male_percentage, male_patients, female_percentage, female_patients):
    return f"""
    <div class="container">
        <div style="display: flex;flex-direction: column; justify-content: center;">
            <div style="text-align: center;
                        color: rgb(0, 34, 101);
                        font-size: 58px;
                        font-family: 'Source Sans Pro';
                        font-weight: bolder;
                        overflow-wrap: break-word;
                        margin-bottom: -16px;">{total_patients}</div>
            <div style="text-align: center;color: rgb(0, 34, 101);font-size: 22px;font-family: 'Source Sans Pro';border-bottom: 0.2px solid #A0A0A0;font-weight: initial;overflow-wrap: break-word;">N°egresos</div>
        </div>
        <div style="background: #D9D9D9; border: 0.60px #A0A0A0"></div>
        <div style="display: flex;flex-direction: row; justify-content: space-around;">
            <div style="display: flex; flex-direction: row ">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ACCEEC" class="w-12 h-12" style="width: 48px; height: auto; margin: 0 auto;">
                        <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
                    </svg>
                <div style="display: flex;flex-direction: column;align-items: center;">
                    <div style="color: rgb(6, 64, 175);
                        font-size: 39px;
                        font-family: system-ui;
                        font-weight: bold;
                        overflow-wrap: break-word;">{male_percentage:.0f}%</div>
                    <div style="text-align: center;
                        color: rgb(6 64 175);
                        font-size: 10px;
                        font-family: system-ui;
                        font-weight: 700;
                        overflow-wrap: break-word;
                        margin-top: -8px;">{male_patients} pacientes</div>
                </div>
            </div>
            <div style="display: flex; flex-direction: row">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#EC4899" class="w-12 h-12" style="width: 48px; height: auto; margin: 0 auto;">
                        <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
                    </svg>
                <div style="display: flex;flex-direction: column;align-items: center;">
                    <div style="color:#7403CC;
                        font-size: 39px;
                        font-family: system-ui;
                        font-weight: bold;
                        overflow-wrap: break-word;">{female_percentage:.0f}%</div>
                    <div style="text-align: center;
                        color: rgb(6 64 175);
                        font-size: 10px;
                        font-family: system-ui;
                        font-weight: 700;
                        overflow-wrap: break-word;
                        margin-top: -8px;">{female_patients} pacientes</div>
                </div>
            </div>
        </div>
    </div>
    """
