// 차트를 업데이트하는 함수
function updateChart(game, data) {
    // 데이터 구조에서 파일명 대신 사용될 범례 이름을 설정합니다.
    const fileNameToLegend = {
        'redwonbin.jpg': '탈모 원빈',
        'hairgwanggyu.jpg': '풍성한 김광규',
        'body.jpg': '목욕탕에서 불 났을 때 중요 부위만 가리고 나오기',
        'face.jpg': '목욕탕에서 불 났을 때 얼굴만 가리고 나오기',
        'memory.jpg': '행복한 기억',
        '71.jpg': '행복한 71억',
        'redkarina.jpg': '카리나',
        'winter.jpg': '윈터',
        'songface.jpg': '다시 태어난다면 송강',
        'lee.jpg': '다시 태어난다면 이재용',
        'now.jpg': '지금 얼굴로 살기',
        '1000million.jpg': '10억 받고 랜덤 돌리기',
        'rebirth_female.jpg': '다시 태어난다면 여자로 태어나기',
        'rebirth_male.jpg': '다시 태어난다면 남자로 태어나기',
        '2seul.jpg': '얼굴은 이상형인데 양아치 여친(남친)',
        '1jin.jpg': '양아치인데 성격은 이상형인 여친(남친)',
        'yoajung.jpg': '요아정',
        'sulbing.jpg': '설빙',
        'empty_brain.jpg': '머리가 빈 애인',
        'skinhead.jpg': '머리카락이 빈 애인'
    };


    '#FFC0CB', '#87CEEB'


    // 각 범례에 대해 색상을 설정합니다.
    const legendToColor = {
        '탈모 원빈': '#FFC0CB',
        '풍성한 김광규': '#87CEEB',
        '목욕탕에서 불 났을 때 중요 부위만 가리고 나오기': '#FFC0CB',
        '목욕탕에서 불 났을 때 얼굴만 가리고 나오기': '#87CEEB',
        '행복한 기억': '#FFC0CB',
        '행복한 71억': '#87CEEB',
        '카리나': '#FFC0CB',
        '윈터': '#87CEEB',
        '다시 태어난다면 송강': '#FFC0CB',
        '다시 태어난다면 이재용': '#87CEEB',
        '지금 얼굴로 살기': '#FFC0CB',
        '10억 받고 랜덤 돌리기': '#87CEEB',
        '다시 태어난다면 여자로 태어나기': '#FFC0CB',
        '다시 태어난다면 남자로 태어나기': '#87CEEB',
        '얼굴은 이상형인데 양아치 여친(남친)': '#FFC0CB',
        '양아치인데 성격은 이상형인 여친(남친)': '#87CEEB',
        '요아정': '#FFC0CB',
        '설빙': '#87CEEB',
        '머리가 빈 애인': '#FFC0CB',
        '머리카락이 빈 애인': '#87CEEB'
    };


    var xValues = Object.keys(data[game]);
    var yValues = Object.values(data[game]);

    // 파일명 대신 범례 이름을 사용하도록 변환합니다.
    var labels = xValues.map(fileName => fileNameToLegend[fileName] || fileName);
    var colors = labels.map(label => legendToColor[label] || '#D3D3D3'); // 기본 색상 설정

    // // 특정 게임의 데이터와 색상 배열을 역순으로 설정합니다.
    // if (game === 'Game 2') {
    //     xValues.reverse();
    //     yValues.reverse();
    // }

    var trace = {
        labels: labels, // 파이 차트에서는 'labels'와 'values'를 사용합니다.
        values: yValues,
        type: 'pie',
        insidetextorientation: 'radial',
        marker: {
            colors: colors
            // colors: ['#FFC0CB', '#87CEEB'] // 사용자 정의 색상 배열
        }
    };

    var layout = {
        showlegend: false
    };

    var config = { responsive: true };

    Plotly.newPlot('chart-' + game, [trace], layout, config);
}

// 모든 차트를 업데이트하는 함수
function fetchDataAndUpdateCharts(gameSequence) {
    fetch('/update_data')
        .then(response => response.json())
        .then(data => {
            gameSequence.forEach(game => {
                updateChart(game, data);
            });
        });
}

// 페이지 로드 시 모든 차트를 업데이트
function initializeCharts(gameSequence) {
    // 초기 차트 업데이트
    fetchDataAndUpdateCharts(gameSequence);

    // 3초마다 차트 업데이트
    setInterval(() => {
        fetchDataAndUpdateCharts(gameSequence);
    }, 3000);
}
