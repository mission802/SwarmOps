# -*- coding:utf-8 -*-
#
# SwarmOps views for api
#

from flask import Blueprint, request, g, abort
from flask_restful import Api, Resource
from utils.public import logger


class Swarm(Resource):

    def get(self):
        """ 查询存储的swarm集群信息 """

        get    = request.args.get("get")
        state  = True if request.args.get("state", False) in ('true', 'True', True) else False
        update = True if request.args.get("UpdateManager", False) in ('true', 'True', True) else False

        if g.auth:
            return g.swarm.GET(get, checkState=state, UpdateManager=update)
        else:
            return abort(403)

    def post(self):
        """ 向存储里添加一个swarm集群 """

        swarmname = request.form.get("name")
        swarmip   = request.form.get("ip")

        if g.auth:
            return g.swarm.POST(swarmName=swarmname, swarmIp=swarmip)
        else:
            return abort(403)

    def put(self):
        """ 设置活跃集群 """

        setActive = True if request.args.get("setActive") in ("true", "True", True) else False
        swarmname = request.args.get("name")

        if g.auth:    
            return g.swarm.PUT(name=swarmname, setActive=setActive)
        else:
            return abort(403)

    def delete(self):
        """ 删除存储中的一个swarm集群 """

        swarmname = request.args.get("name", request.form.get("name"))

        if g.auth:    
            return g.swarm.DELETE(name=swarmname)
        else:
            return abort(403)

class Service(Resource):

    def get(self):
        """ 查询swarm活跃集群集群service信息 """

        service = request.args.get("id", request.args.get("name", None))
        core    = True if request.args.get("core", True) in ("True", "true", True) else False
        core_convert = True if request.args.get("core_convert", True) in ("True", "true", True) else False
        getNode = True if request.args.get("getNode", False) in ("True", "true", True) else False
        getBackend = True if request.args.get("getBackend", False) in ("True", "true", True) else False

        if g.auth:
            if getNode or getBackend:
                return g.service.GetServiceNode(serviceId=service, getBackend=getBackend)
            else:
                return g.service.GET(service, core, core_convert)
        else:
            return abort(403)

    def post(self):
        """ 创建服务 """

        #get query, optional only is "name, env, mount, publish, replicas", required "image".
        image     = request.form.get("image")
        name      = request.form.get("name")
        env       = request.form.get("env")
        mount     = request.form.get("mount")        
        publish   = request.form.get("publish")
        replicas  = request.form.get("replicas") or 1
        if g.auth:
            return g.service.POST(image=image,name=name,env=env,mount=mount,publish=publish,replicas=replicas)
        else:
            return abort(403)

    def put(self):
        """ 更新服务 """

        flag        = request.form.get("flag", request.form.get("serviceId", request.form.get("serviceName")))
        #In fact, the official currently only supports the ID form of the update operation.
        image       = request.form.get("image")
        name        = request.form.get("name")
        env         = request.form.get("env")
        mount       = request.form.get("mount")    
        publish     = request.form.get("publish")
        replicas    = request.form.get("replicas")
        delay       = request.form.get("delay")
        parallelism = request.form.get("parallelism")
        USType      = request.form.get("UpdateServiceType", "api")

        if g.auth:
            return g.service.PUT(serviceFlag=flag, image=image, name=name, env=env, mount=mount, publish=publish, replicas=replicas, delay=delay, parallelism=parallelism, UpdateServiceType=USType)
        else:
            return abort(403)

    def delete(self):
        """ 删除服务 """

        flag = request.form.get("flag", request.form.get("serviceId", request.form.get("serviceName", request.form.get("id", request.form.get("name")))))

        if g.auth:
            return g.service.DELETE(serviceFlag=flag)
        else:
            return abort(403)

class Node(Resource):

    def get(self):
        """ 查询节点 """

        if g.auth:
            return g.node.GET(node=request.args.get("node", None))
        else:
            return abort(403)

    def post(self):
        """ 加入一个swarm集群 """

        ip   = request.form.get("ip")
        role = request.form.get("role", "Worker")
        logger.info(request.form)

        if g.auth:
            return g.node.POST(ip=ip, role=role)
        else:
            return abort(403)

    def delete(self):
        """ 节点离开集群 """

        node_ip = request.form.get("ip")
        force  = True if request.form.get("force") in ("true", "True", True) else False

        if g.auth:
            return g.node.DELETE(ip=node_ip, force=force)
        else:
            return abort(403)

    def put(self):
        """ 更新节点信息(Labels、Role等) """

        node_id     = request.form.get("node_id")
        node_role   = request.form.get("node_role")
        node_labels = request.form.get("node_labels")
        logger.debug("{}, {}, {}".format(node_id, node_role, node_labels))

        if g.auth:
            return g.node.PUT(node_id=node_id, node_role=node_role, node_labels=node_labels)
        else:
            return abort(403)

class InitSwarm(Resource):

    def post(self):
        """ 向存储里添加一个swarm集群 """

        ip    = request.form.get("ip")
        force = True if request.form.get("force", False) in ("true", "True", True) else False

        if g.auth:
            return g.swarm.InitSwarm(AdvertiseAddr=ip, ForceNewCluster=force)
        else:
            return abort(403)

class Network(Resource):

    def get(self):
        """ 查询网络 """

        if g.auth:
            return g.network.GET(networkId=request.args.get("networkId", None))
        else:
            return abort(403)

    def post(self):
        """ 创建网络 """

        ip   = request.form.get("ip")
        role = request.form.get("role", "Worker")
        logger.info(request.form)

        if g.auth:
            return g.node.POST(ip=ip, role=role)
        else:
            return abort(403)

    def delete(self):
        """ 删除网络 """

        node_ip = request.form.get("ip")
        force  = True if request.form.get("force") in ("true", "True", True) else False

        if g.auth:
            return g.node.DELETE(ip=node_ip, force=force)
        else:
            return abort(403)

class Registry(Resource):

    def get(self):
        """ 查询私有仓 """

        query     = request.args.get("q")
        ImageName = request.args.get("ImageName")
        ImageId   = request.args.get("ImageId")
        tag       = request.args.get("tag")

        if g.auth:
            res = {"msg": None, "data": None}
            if query == "url":
                res.update(data=g.registry.url)
            elif query == "status":
                res.update(data=g.registry.status)
            elif query == "version":
                res.update(data=g.registry.version)
            elif query == "all_repository":
                res.update(data=g.registry._list_all_repository)
            elif query == "all_tag":
                res.update(data=g.registry._list_repository_tag(ImageName))
            elif query == "all_imageId_ancestry":
                res.update(data=g.registry._list_imageId_ancestry(ImageId))
            elif query == "imageId_info":
                res.update(data=g.registry._get_imageId_info(ImageId))
            logger.info(res)
            return res
        else:
            return abort(403)

    def delete(self):
        """ 删除镜像<标签> """

        repository_name     = request.args.get("repository_name")
        repository_name_tag = request.args.get("repository_name_tag")

        if g.auth:
            res = {"msg": None, "success": False}
            if repository_name_tag:
                res.update(success=g.registry._delete_repository_tag(ImageName=repository_name, tag=repository_name_tag))
            else:
                res.update(success=g.registry._delete_repository(ImageName=repository_name))
            logger.info(res)
            return res
        else:
            return abort(403)

class RollingUpgradeService(Resource):

    def post(self):
        """ 滚动升级服务 """

        tag = request.form.get("tag")
        sid = request.form.get("serviceId")

        if g.auth:
            return g.service.RollingUpgrade(serviceFlag=sid, tag=tag)
        else:
            return abort(403)

core_blueprint = Blueprint(__name__, __name__)
api = Api(core_blueprint)
api.add_resource(Swarm, '/swarm', '/swarm/', endpoint='swarm')
api.add_resource(Service, '/service', '/service/', endpoint='service')
api.add_resource(Node, '/node', '/node/', endpoint='node')
api.add_resource(InitSwarm, '/swarm/init', '/swarm/init/', endpoint='InitSwarm')
api.add_resource(Network, '/network', '/network/', endpoint='network')
api.add_resource(Registry, '/registry', '/registry/', endpoint='registry')
api.add_resource(RollingUpgradeService, '/rollingupgradeservice', '/rollingupgradeservice/', endpoint='rollingupgradeservice')
