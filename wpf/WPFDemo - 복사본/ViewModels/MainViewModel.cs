using Caliburn.Micro;
using System;
using System.Text;
using WPFDemo.Helper;
//using Newtonsoft.Json;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;



namespace WPFDemo.ViewModels
{
    class MainViewModel : Conductor<object> //Screen에는 ActivateItem[Async]메서드가 없음.
    {
        public MainViewModel()
        {
            DisplayName = "SmartHome Monitoring v2.0";  //title 설정

            BrokerUrl = Commons.BROKERHOST = "210.119.12.70";   //MQTT Broker IP 설정

            ConnString = Commons.CONNSTRING = "Data Source=PC01\\SQLEXPRESS;Initial Catalog=OpenApiLab;Integrated Security=True";

            if (Commons.IS_CONNECT)
            {
                IsConnected = true;
                ConnectDb();
            }
        }

        //protected override Task OnDeactivateAsync(bool close, CancellationToken cancellationToken)
        //{
        //    if (Commons.MQTT_CLIENT.IsConnected)
        //    {
        //        Commons.MQTT_CLIENT.Disconnect();
        //        Commons.MQTT_CLIENT = null;
        //    }//비활성화 처리
        //    return base.OnDeactivateAsync(close, cancellationToken);
        //}



        private string brokerUrl;
        private string topic;
        private string connString;
        private string dbLog;
        private bool isConnected;

        public string BrokerUrl
        {
            get { return brokerUrl; }
            set
            {
                brokerUrl = value;
                NotifyOfPropertyChange(() => BrokerUrl);

            }
        }


        public string Topic
        {
            get { return topic; }
            set
            {
                topic = value;
                NotifyOfPropertyChange(() => Topic);
            }
        }



        public string ConnString
        {
            get => connString;

            set
            {
                connString = value;
                NotifyOfPropertyChange(() => ConnString);
            }
        }


        public string DbLog
        {
            get => dbLog;
            set
            {
                dbLog = value;
                NotifyOfPropertyChange(() => DbLog);
            }
        }

        public bool IsConnected
        {
            get => isConnected;
            set
            {
                isConnected = value;
                NotifyOfPropertyChange(() => IsConnected);
            }
        }



        /// <summary>
        /// DB연결 + MQTT 접속
        /// </summary>
        public void ConnectDb()
        {
            if (IsConnected)
            {
                Commons.MQTT_CLIENT = new MqttClient(BrokerUrl);

                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected != true)
                    {
                        var winManager = new WindowManager();
                        var result = winManager.ShowDialogAsync(new CustomPopupViewModel("New Broker"));
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.PUB_TOPIC },
                            new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE });

                        UpdateText(">>> MQTT Broker Connected");
                        IsConnected = Commons.IS_CONNECT = true;
                    }
                }
                catch (Exception ex)
                {
                    //Pass

                }

            }
            else
            {
                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateText(">>> MQTT Broker Disconnected");
                        IsConnected = Commons.IS_CONNECT = false;
                    }
                }
                catch (Exception)
                {

                    //throw;
                }
            }

        }

        private void UpdateText(string message)
        {
            DbLog += $"{message}\n";
        }

        /// <summary>
        /// Subscribe한 메세지 처리 이벤트 핸들러
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var message = Encoding.UTF8.GetString(e.Message);   //bite형식으로 날라온 글짜 다시 string 형으로 바꿔
            UpdateText(message);    //센서데이터 출력
            //SetDataBase(message, e.Topic);   //DB에 저장

        }

    }

}
