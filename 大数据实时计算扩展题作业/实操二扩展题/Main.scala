import java.util.{Properties, UUID}

import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.streaming.api.functions.ProcessFunction
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer010
import org.apache.flink.util.Collector

import scala.collection.mutable
import scala.util.parsing.json.JSON

object Main {
  /**
   * 输入的主题名称
   */
  val inputTopic = "mn_buy_ticket_demo2"
  /**
   * kafka地址
   */
  val bootstrapServers = "bigdata35.depts.bingosoft.net:29035,bigdata36.depts.bingosoft.net:29036,bigdata37.depts.bingosoft.net:29037"

  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setParallelism(1)
    env.setMaxParallelism(1)
    val kafkaProperties = new Properties()
    kafkaProperties.put("bootstrap.servers", bootstrapServers)
    kafkaProperties.put("group.id", UUID.randomUUID().toString)
    kafkaProperties.put("auto.offset.reset", "earliest")
    kafkaProperties.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    kafkaProperties.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    val kafkaConsumer = new FlinkKafkaConsumer010[String](inputTopic,
      new SimpleStringSchema, kafkaProperties)
    kafkaConsumer.setCommitOffsetsOnCheckpoints(true)
    val inputKafkaStream = env.addSource(kafkaConsumer)

    def regJson(json: Option[Any]) = json match {
      case Some(map: Map[String, Any]) => map
    }

    def getStr(x: Option[Any]) = x match {
      case Some(s) => s
      case None => "?"
    }

    inputKafkaStream.map(
      jsonStr => {
        val jsonAny = JSON.parseFull(jsonStr)
        val jsonObject = regJson(jsonAny)
        getStr(jsonObject.get("destination"))
      }
    ).process(new ProcessFunction[Any, String] {
      var cntMap = new mutable.HashMap[Any, Int]()
      var top5cities: Seq[(Any, Int)] = _

      override def processElement(i: Any, context: ProcessFunction[Any, String]#Context, collector: Collector[String]): Unit = {
        if (cntMap.contains(i)) {
          val cnt = cntMap.apply(i)
          cntMap.put(i, cnt + 1)
        }
        else {
          cntMap.put(i, 1)
        }
        val newTop5cities = cntMap.toSeq.sortWith(_._2 > _._2).take(4)
        if (newTop5cities != top5cities) {
          top5cities = newTop5cities
          println("乘客到达数前5城市：" + top5cities)
        }

      }

    })


    env.execute()
  }

}