import java.sql.{ResultSet, SQLException}
import java.util.Properties

import com.bingocloud.auth.BasicAWSCredentials
import com.bingocloud.services.s3.AmazonS3Client
import com.bingocloud.util.json.JSONException
import com.bingocloud.{ClientConfiguration, Protocol}
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import org.json._
import org.nlpcn.commons.lang.util.IOUtil

object Main {
  //s3参数
  val accessKey = "8A5290742BF72419BAFF"
  val secretKey = "W0FGNTc5OTU0RkJEQjQ3RTZCQTA2MjgxOEYwRUY2RkREQ0JBMzI1NTRd"
  val endpoint = "scuts3.depts.bingosoft.net:29999"
  val bucket = "hezhiwei"
  //要读取的文件
  val key = "demo.txt"

  //kafka参数
  val topic = "hezhiwei"
  val bootstrapServers = "bigdata35.depts.bingosoft.net:29035,bigdata36.depts.bingosoft.net:29036,bigdata37.depts.bingosoft.net:29037"

  def main(args: Array[String]): Unit = {
    val tableContent = getTableFromMysql()
    produceToKafka(tableContent)
  }

  /**
   * 从s3中读取文件内容
   *
   * @return s3的文件内容
   */
  def readFile(): String = {
    val credentials = new BasicAWSCredentials(accessKey, secretKey)
    val clientConfig = new ClientConfiguration()
    clientConfig.setProtocol(Protocol.HTTP)
    val amazonS3 = new AmazonS3Client(credentials, clientConfig)
    amazonS3.setEndpoint(endpoint)
    val s3Object = amazonS3.getObject(bucket, key)
    IOUtil.getContent(s3Object.getObjectContent, "UTF-8")
  }

  /**
   * 从Mysql获取表数据
   *
   */
  def getTableFromMysql(): String = {
    import java.sql.DriverManager
    val url = "jdbc:mysql://bigdata28.depts.bingosoft.net:23307/user19_db"

    val properties = new Properties()
    properties.setProperty("driverClassName", "com.mysql.jdbc.Driver")
    properties.setProperty("user", "user19")
    properties.setProperty("password", "pass@bingo19")

    val connection = DriverManager.getConnection(url, properties)
    val statement = connection.createStatement
    val resultSet = statement.executeQuery("select * from t_rk_jbxx_result_2")
    try {

      val res = resultSetToJson(resultSet)
      resultSet.close()
      res
    } catch {
      case e: Exception => e.printStackTrace()
        return "0"
    }
  }


  /**
   * 将mysql的result set转为json字符串格式
   *
   * @param rs result set
   */
  @throws[SQLException]
  @throws[JSONException]
  def resultSetToJson(rs: ResultSet): String = { // json数组
    val array = new JSONArray()
    // 获取列数
    val metaData = rs.getMetaData
    val columnCount = metaData.getColumnCount
    // 遍历ResultSet中的每条数据
    while ( {
      rs.next
    }) {
      val jsonObj = new JSONObject();
      // 遍历每一列
      for (i <- 1 to columnCount) {
        val columnName = metaData.getColumnLabel(i)
        val value = rs.getString(columnName)
        jsonObj.put(columnName, value)
      }
      array.put(jsonObj)
    }

    var res = ""
    for (k <- 0 until array.length()) {
      res = res + array.get(k).toString + '\n'
    }
    res
  }


  /**
   * 把数据写入到kafka中
   *
   * @param s3Content 要写入的内容
   */
  def produceToKafka(s3Content: String): Unit = {
    val props = new Properties
    props.put("bootstrap.servers", bootstrapServers)
    props.put("acks", "all")
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    val producer = new KafkaProducer[String, String](props)
    val dataArr = s3Content.split("\n")
    for (s <- dataArr) {
      if (!s.trim.isEmpty) {
        val record = new ProducerRecord[String, String](topic, null, s)
        println("开始生产数据：" + s)
        producer.send(record)
      }
    }
    producer.flush()
    producer.close()
  }
}