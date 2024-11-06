namespace go api


service HelloService {
    string Hello(1: string name) (api.get="/hello");
}