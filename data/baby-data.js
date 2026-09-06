(function () {
  "use strict";
  const milestone = (id, month, order, title, subtitle, description, sourceDate) => ({
    id, month, order, type: "milestone", importance: 3, layout: order % 2 ? "right-media" : "left-media",
    align: order % 2 ? "right" : "left", title, subtitle, description, sourceDate, media: []
  });
  window.BABY_DISCOVERY_DATA = {
    version: "1.0.0", technicalBabyId: "ca",
    profile: {
      id: "y-khue", sourceId: "be-tom", sourceAlias: "Bé Dần", name: "Tsàn Ý Khuê", initials: "YK", hanzi: "秦懿奎",
      birthDate: "2022-12-08", birthTime: "07:10", birthLunar: "15/11/2022", birthLunarLabel: "Âm lịch · ngày rằm",
      accent: "#4F9271", accentWarm: "#8FC7AE", backgroundAsset: "./assets/y-khue/ui/journey-background.svg",
      shortBio: "Một cô bé lanh lợi, hoạt bát, thích khám phá, vận động và những hoạt động thực hành như lắp ghép.",
      nameMeaning: "Ý gắn với đức độ, ôn hòa, nhu mì, sáng láng. Khuê gắn với trí tuệ, nghị lực, văn chương học thuật và sự tỏa sáng tựa sao Khuê. Ý nghĩa gia đình: người con gái nữ tính ôn hòa, nhu mì, xinh đẹp, thông minh tỏa sáng như vì sao Khuê.",
      personality: ["Lanh lợi", "Hiếu động", "Thích khám phá", "Thích vận động", "Khéo tay"],
      strengths: ["Vận động", "Lắp ghép", "Thực hành"], interests: ["Lắp ghép", "Xe đồ chơi", "Chạy nhảy", "Khám phá ngoài trời"]
    },
    backgrounds: [
      {id:"waiting",fromMonth:-12,toMonth:0,label:"Chờ con chào đời",gradient:"radial-gradient(circle at 20% 18%,rgba(143,199,174,.55),transparent 34%),linear-gradient(#f5faf5,#edf6ef)"},
      {id:"birth",fromMonth:0,toMonth:12,label:"Chào đời",gradient:"radial-gradient(circle at 80% 16%,rgba(143,199,174,.56),transparent 34%),linear-gradient(#f5faf5,#eaf5ee)"},
      {id:"discover",fromMonth:12,toMonth:24,label:"Khám phá",gradient:"radial-gradient(circle at 18% 22%,rgba(164,216,190,.55),transparent 34%),linear-gradient(#f2faf4,#edf7f0)"},
      {id:"independence",fromMonth:24,toMonth:36,label:"Tự lập",gradient:"radial-gradient(circle at 80% 25%,rgba(105,173,132,.30),transparent 34%),linear-gradient(#f4fbf5,#e9f4ec)"},
      {id:"learning",fromMonth:36,toMonth:120,label:"Học và khám phá",gradient:"radial-gradient(circle at 22% 18%,rgba(79,146,113,.25),transparent 34%),linear-gradient(#f3faf5,#e7f3eb)"}
    ],
    health: [
      {id:"HLT-CA-001",month:25,date:"2025-01-25",ageText:"2 tuổi 1 tháng",heightCm:91,weightKg:13.7,bmi:16.54},
      {id:"HLT-CA-002",month:26,date:"2025-02-22",ageText:"2 tuổi 2 tháng",heightCm:91,weightKg:13.7,bmi:16.54},
      {id:"HLT-CA-003",month:27,date:"2025-04-01",ageText:"2 tuổi 3 tháng",heightCm:91,weightKg:14.35,bmi:17.33},
      {id:"HLT-CA-004",month:28,date:"2025-05-07",ageText:"2 tuổi 4 tháng",heightCm:93.5,weightKg:14.85,bmi:16.99},
      {id:"HLT-CA-005",month:30,date:"2025-07-04",ageText:"2 tuổi 6 tháng",heightCm:96.5,weightKg:15.1,bmi:16.22},
      {id:"HLT-CA-006",month:34,date:"2025-11-02",ageText:"2 tuổi 10 tháng",heightCm:98,weightKg:16.2,bmi:16.87},
      {id:"HLT-CA-007",month:36,date:"2025-12-30",ageText:"3 tuổi",heightCm:103,weightKg:16,bmi:15.08},
      {id:"HLT-CA-008",month:42,date:"2026-06-27",ageText:"3 tuổi 6 tháng",heightCm:104,weightKg:16.5,bmi:15.26},
      {id:"HLT-CA-009",month:43,date:"2026-07-22",ageText:"3 tuổi 7 tháng",heightCm:104,weightKg:17.35,bmi:16.04}
    ],
    scenes: [
      {id:"ca-prenatal",month:-4,order:0,type:"memory",importance:4,layout:"hero",align:"center",eyebrow:"TRƯỚC NGÀY CON CHÀO ĐỜI",title:"Chờ con chào đời",subtitle:"Những hình ảnh được gia đình lưu trước ngày sinh",description:"Những kỷ niệm trước ngày 08/12/2022 được giữ thành một đoạn riêng, không quy đổi thành tuổi của bé.",sourceRole:"dated-media",media:[]},
      {id:"ca-birth",month:0,order:0,type:"birth",importance:5,layout:"hero",align:"center",date:"2022-12-08",eyebrow:"08 · 12 · 2022",title:"Ý Khuê chào đời",subtitle:"Khởi đầu của một hành trình lớn lên",description:"Tsàn Ý Khuê chào đời lúc 07:10 sáng ngày 08/12/2022. Từ ngày ấy, hành trình lớn lên của Cá bắt đầu.",sourceRole:"user-confirmed",media:[]},
      milestone("ca-03m-flip",3,1,"Biết lật","Những chuyển động đầu tiên","Mốc vận động gia đình ghi nhận ở giai đoạn 3 tháng tuổi.","2023-03-08"),
      milestone("ca-06m-sleep",6,2,"Tự ngủ","Những giấc ngủ đầu đời","Gia đình ghi nhận Cá có thể tự đi vào giấc ngủ và ngủ một giấc tới sáng ở giai đoạn khoảng 6 tháng.","2023-06-08"),
      milestone("ca-11m-walk",11,3,"Đi vững bằng hai chân","Tự tin bước đi","Gia đình ghi nhận Cá đi vững trong khoảng 11 đến 12 tháng tuổi.","2023-11-08"),
      milestone("ca-12m-diaper",12,4,"Không còn dùng tã","Một nếp sinh hoạt tự lập","Gia đình ghi nhận cột mốc sinh hoạt này lúc 12 tháng.","2023-12-08"),
      milestone("ca-12m-night",12,5,"Ngủ tới sáng","Đêm trọn giấc","Gia đình ghi nhận Cá ngủ tới sáng và chủ động đi vệ sinh trước khi ngủ ở giai đoạn 1 tuổi.","2023-12-08"),
      milestone("ca-14m-pacifier",14,6,"Cai ti giả","Thay đổi một thói quen","Gia đình ghi nhận Cá cai ti giả lúc 14 tháng.","2024-02-08"),
      milestone("ca-24m-letters",24,7,"Làm quen với chữ cái","Tô chữ và tập viết","Ở giai đoạn 2 tuổi, Cá bắt đầu tô chữ, viết bài và nhận biết các chữ cái cơ bản.","2024-12-08"),
      milestone("ca-24m-clothes",24,8,"Tự lấy và mặc quần áo","Từng việc nhỏ của sự tự lập","Gia đình ghi nhận Cá tự lấy, mặc và cởi quần áo ở giai đoạn 2 tuổi.","2024-12-08"),
      milestone("ca-24m-wash",24,9,"Tập tắm gội","Chăm sóc bản thân","Ghi chép gia đình về việc Cá tập tắm gội bằng xà bông ở giai đoạn 2 tuổi; cần được đối chiếu thêm nếu bổ sung media.","2024-12-08"),
      milestone("ca-24m-toilet",24,10,"Tự đi vệ sinh","Một nếp sinh hoạt mới","Gia đình ghi nhận Cá biết tự đi vệ sinh và thức dậy khi cần vào giai đoạn 2 tuổi.","2024-12-08"),
      milestone("ca-25m-fish",25,11,"Vẽ hình con cá","Một nét vẽ được ghi lại","Ngày 14/01/2025, gia đình ghi nhận Cá vẽ được hình con cá.","2025-01-14"),
      milestone("ca-reward",30,12,"Mỗi bài học, một đồng","Bài học nhỏ về phần thưởng","Cá tham gia hệ thống thưởng của gia đình: hoàn thành bài học hoặc nhiệm vụ được thưởng một đồng.","2025-06-01"),
      milestone("ca-toys",30,13,"Niềm vui với đồ chơi mới","Những điều Cá thích","Gia đình ghi nhận Cá thích đồ chơi mới và thường ưu tiên những món mình yêu thích.","2025-06-01"),
      milestone("ca-36m-languages",36,14,"Nói tiếng Việt và tiếng Hoa","Ngôn ngữ lớn dần mỗi ngày","Khi tròn 3 tuổi, gia đình ghi nhận Cá sử dụng tiếng Việt và tiếng Hoa.","2025-12-08"),
      milestone("ca-36m-mimic",36,15,"Khả năng ngôn ngữ và bắt chước","Một cách quan sát riêng","Ngày 09/12/2025, gia đình ghi nhận khả năng ngôn ngữ và bắt chước của Cá.","2025-12-09"),
      milestone("ca-38m-english",38,16,"Làm quen với tiếng Anh","Một ngôn ngữ mới","Ngày 09/02/2026, gia đình ghi nhận Cá đang học tiếng Anh.","2026-02-09"),
      milestone("ca-42m-bike",42,17,"Chạy xe đạp hai bánh","Một đoạn đường mới","Ngày 27/06/2026, khi 3 tuổi 6 tháng 18 ngày, gia đình ghi nhận Cá chạy xe đạp hai bánh.","2026-06-27"),
      milestone("ca-42m-building",42,18,"Thích lắp ghép và vận động","Những hoạt động thực hành","Gia đình ghi nhận Cá thích chơi lắp ráp và các hoạt động vận động.","2026-06-27"),
      milestone("ca-42m-talk",42,19,"Nói chuyện rành rọt, linh hoạt","Cách diễn đạt của riêng Cá","Ngày 03/07/2026, gia đình ghi nhận Cá nói chuyện rành rọt, linh hoạt.","2026-07-03"),
      milestone("ca-42m-learning",42,20,"Học khi có hứng thú","Tập trung vào điều mình thích","Ghi chép gia đình cho biết Cá đang viết bài, học cộng cơ bản và ngồi lâu khi chơi lắp ghép; phần học cần được tiếp tục quan sát.","2026-07-03"),
      milestone("ca-picky-eating",13,21,"Khẩu vị riêng","Những bữa ăn theo sở thích","Gia đình ghi nhận Cá khá kén ăn và ít ăn vặt. Đây là ghi chép sinh hoạt, không phải đánh giá y tế.","2024-01-01")
    ]
  };
})();
